import json
import logging
import time
from typing import (
    Any,
    List,
    Sequence,
    Union,
    Literal,
    cast,
    Optional,
)
from typing import (
    Dict,
    AsyncGenerator,
    Iterable,
)

from fastapi import HTTPException
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    BaseMessage,
    ToolMessage,
)
from langchain_core.messages import AIMessageChunk
from langchain_core.messages.ai import UsageMetadata
from langchain_core.runnables.schema import CustomStreamEvent, StandardStreamEvent
from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode
from openai.types import CompletionUsage
from openai.types.chat import (
    ChatCompletionChunk,
    ChatCompletion,
    ChatCompletionMessage,
    ChatCompletionSystemMessageParam,
)
from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat.chat_completion import Choice
from openai.types.chat.chat_completion_chunk import ChoiceDelta, Choice as ChunkChoice
from starlette.responses import StreamingResponse, JSONResponse

from language_model_gateway.gateway.converters.my_messages_state import MyMessagesState
from language_model_gateway.gateway.schema.openai.completions import (
    ChatRequest,
    ROLE_TYPES,
    INCOMING_MESSAGE_TYPES,
)
from language_model_gateway.gateway.utilities.chat_message_helpers import (
    langchain_to_chat_message,
    convert_message_content_to_string,
)

logger = logging.getLogger(__file__)


class LangGraphToOpenAIConverter:
    async def _stream_resp_async_generator(
        self,
        *,
        request: ChatRequest,
        request_id: str,
        compiled_state_graph: CompiledStateGraph,
        messages: List[ChatCompletionMessageParam],
    ) -> AsyncGenerator[str, None]:
        """
        Asynchronously generate streaming responses from the agent.

        Args:
            request: The chat request.
            request_id: The unique request identifier.
            compiled_state_graph: The compiled state graph.
            messages: The list of chat completion message parameters.

        Yields:
            The streaming response as a string.
        """
        # Process streamed events from the graph and yield messages over the SSE stream.
        event: StandardStreamEvent | CustomStreamEvent
        async for event in self.astream_events(
            request=request,
            compiled_state_graph=compiled_state_graph,
            messages=messages,
        ):
            if not event:
                continue

            event_type: str = event["event"]

            # print(f"===== {event_type} =====\n{event}\n")

            match event_type:
                case "on_chain_start":
                    # Handle the start of the chain event
                    pass
                case "on_chat_model_stream":
                    # Handle the chat model stream event
                    chunk: AIMessageChunk = event["data"]["chunk"]
                    content: str | list[str | dict[str, Any]] = chunk.content

                    # print(f"chunk: {chunk}")

                    usage_metadata: Optional[UsageMetadata] = chunk.usage_metadata
                    total_usage_metadata = self.convert_usage_meta_data_to_openai(
                        usages=[usage_metadata] if usage_metadata else []
                    )

                    content_text: str = convert_message_content_to_string(content)

                    assert isinstance(
                        content_text, str
                    ), f"content_text: {content_text} (type: {type(content_text)})"

                    if content_text:
                        chat_stream_response: ChatCompletionChunk = ChatCompletionChunk(
                            id=request_id,
                            created=int(time.time()),
                            model=request["model"],
                            choices=[
                                ChunkChoice(
                                    index=0,
                                    delta=ChoiceDelta(
                                        role="assistant", content=content_text
                                    ),
                                )
                            ],
                            usage=total_usage_metadata,
                            object="chat.completion.chunk",
                        )
                        yield f"data: {json.dumps(chat_stream_response.model_dump())}\n\n"
                case "on_chain_end":
                    # Handle the end of the chain event
                    pass
                case "on_tool_end":
                    # Handle the end of the tool event
                    tool_message: ToolMessage = event["data"]["output"]

                    artifact: Optional[Any] = tool_message.artifact

                    # print(f"on_tool_end: {tool_message}")

                    if artifact:
                        chat_stream_response = ChatCompletionChunk(
                            id=request_id,
                            created=int(time.time()),
                            model=request["model"],
                            choices=[
                                ChunkChoice(
                                    index=0,
                                    delta=ChoiceDelta(
                                        role="assistant", content=artifact
                                    ),
                                )
                            ],
                            usage=CompletionUsage(
                                prompt_tokens=0, completion_tokens=0, total_tokens=0
                            ),
                            object="chat.completion.chunk",
                        )
                        yield f"data: {json.dumps(chat_stream_response.model_dump())}\n\n"
                case _:
                    # Handle other event types
                    pass

        yield "data: [DONE]\n\n"

    async def call_agent_with_input(
        self,
        *,
        request: ChatRequest,
        request_id: str,
        compiled_state_graph: CompiledStateGraph,
        system_messages: List[ChatCompletionSystemMessageParam],
    ) -> StreamingResponse | JSONResponse:
        """
        Call the agent with the provided input and return the response.

        Args:
            request: The chat request.
            request_id: The unique request identifier.
            compiled_state_graph: The compiled state graph.
            system_messages: The list of chat completion message parameters.

        Returns:
            The response as a StreamingResponse or JSONResponse.
        """
        assert request is not None
        assert isinstance(request, dict)

        if request.get("stream"):
            return StreamingResponse(
                await self.get_streaming_response_async(
                    request=request,
                    request_id=request_id,
                    compiled_state_graph=compiled_state_graph,
                    system_messages=system_messages,
                ),
                media_type="text/event-stream",
            )
        else:
            try:
                responses: List[AnyMessage] = await self.ainvoke(
                    compiled_state_graph=compiled_state_graph,
                    request=request,
                    system_messages=system_messages,
                )
                # add usage metadata from each message into a total usage metadata
                total_usage_metadata: CompletionUsage = (
                    self.convert_usage_meta_data_to_openai(
                        usages=[
                            m.usage_metadata
                            for m in responses
                            if hasattr(m, "usage_metadata") and m.usage_metadata
                        ]
                    )
                )

                output_messages_raw: List[ChatCompletionMessage | None] = [
                    langchain_to_chat_message(m)
                    for m in responses
                    if isinstance(m, AIMessage) or isinstance(m, ToolMessage)
                ]
                output_messages: List[ChatCompletionMessage] = [
                    m for m in output_messages_raw if m is not None
                ]

                choices: List[Choice] = [
                    Choice(index=i, message=m, finish_reason="stop")
                    for i, m in enumerate(output_messages)
                ]
                chat_response: ChatCompletion = ChatCompletion(
                    id=request_id,
                    model=request["model"],
                    choices=choices,
                    usage=total_usage_metadata,
                    created=int(time.time()),
                    object="chat.completion",
                )
                return JSONResponse(content=chat_response.model_dump())
            except Exception as e:
                logger.error(f"An exception occurred: {e}")
                raise HTTPException(status_code=500, detail="Unexpected error")

    # noinspection PyMethodMayBeStatic
    def convert_usage_meta_data_to_openai(
        self, *, usages: List[UsageMetadata]
    ) -> CompletionUsage:
        total_usage_metadata: CompletionUsage = CompletionUsage(
            prompt_tokens=0, completion_tokens=0, total_tokens=0
        )
        usage_metadata: UsageMetadata
        for usage_metadata in usages:
            total_usage_metadata.prompt_tokens += usage_metadata["input_tokens"]
            total_usage_metadata.completion_tokens += usage_metadata["output_tokens"]
            total_usage_metadata.total_tokens += usage_metadata["total_tokens"]
        return total_usage_metadata

    async def get_streaming_response_async(
        self,
        *,
        request: ChatRequest,
        request_id: str,
        compiled_state_graph: CompiledStateGraph,
        system_messages: List[ChatCompletionSystemMessageParam],
    ) -> AsyncGenerator[str, None]:
        """
        Get the streaming response asynchronously.

        Args:
            request: The chat request.
            request_id: The unique request identifier.
            compiled_state_graph: The compiled state graph.
            system_messages: The list of chat completion message parameters.

        Returns:
            The streaming response as an async generator.
        """

        new_messages: List[ChatCompletionMessageParam] = [
            m for m in request["messages"]
        ]
        messages: List[ChatCompletionMessageParam] = [
            s for s in system_messages
        ] + new_messages

        logger.info(f"Streaming response {request_id} from agent")
        generator: AsyncGenerator[str, None] = self._stream_resp_async_generator(
            request=request,
            request_id=request_id,
            compiled_state_graph=compiled_state_graph,
            messages=messages,
        )
        return generator

    # noinspection PyMethodMayBeStatic
    async def _run_graph_with_messages_async(
        self,
        *,
        messages: List[tuple[ROLE_TYPES, INCOMING_MESSAGE_TYPES]],
        compiled_state_graph: CompiledStateGraph,
    ) -> List[AnyMessage]:
        """
        Run the graph with the provided messages asynchronously.

        Args:
            messages: The list of role and incoming message type tuples.
            compiled_state_graph: The compiled state graph.

        Returns:
            The list of any messages.
        """
        input1: Dict[str, List[tuple[ROLE_TYPES, INCOMING_MESSAGE_TYPES]]] = {
            "messages": messages
        }
        output: Dict[str, Any] = await compiled_state_graph.ainvoke(input=input1)
        out_messages: List[AnyMessage] = output["messages"]
        return out_messages

    # noinspection PyMethodMayBeStatic
    async def _stream_graph_with_messages_async(
        self,
        *,
        request: ChatRequest,
        messages: List[tuple[ROLE_TYPES, INCOMING_MESSAGE_TYPES]],
        compiled_state_graph: CompiledStateGraph,
    ) -> AsyncGenerator[StandardStreamEvent | CustomStreamEvent, None]:
        """
        Stream the graph with the provided messages asynchronously.

        Args:
            request: The chat request.
            messages: The list of role and incoming message type tuples.
            compiled_state_graph: The compiled state graph.

        Yields:
            The standard or custom stream event.
        """
        input1: Dict[str, List[tuple[ROLE_TYPES, INCOMING_MESSAGE_TYPES]]] = {
            "messages": messages
        }
        event: StandardStreamEvent | CustomStreamEvent
        async for event in compiled_state_graph.astream_events(
            input=input1, version="v2"
        ):
            yield event

    # noinspection SpellCheckingInspection
    async def ainvoke(
        self,
        *,
        request: ChatRequest,
        compiled_state_graph: CompiledStateGraph,
        system_messages: Iterable[ChatCompletionSystemMessageParam],
    ) -> List[AnyMessage]:
        """
        Run the agent asynchronously.

        Args:
            request: The chat request.
            compiled_state_graph: The compiled state graph.
            system_messages: The iterable of chat completion message parameters.

        Returns:
            The list of any messages.
        """
        assert request is not None
        assert isinstance(request, dict)

        new_messages: List[ChatCompletionMessageParam] = [
            m for m in request["messages"]
        ]
        messages: List[ChatCompletionMessageParam] = [
            s for s in system_messages
        ] + new_messages

        return await self._run_graph_with_messages_async(
            compiled_state_graph=compiled_state_graph,
            messages=self.create_messages_for_graph(messages=messages),
        )

    async def astream_events(
        self,
        *,
        request: ChatRequest,
        compiled_state_graph: CompiledStateGraph,
        messages: Iterable[ChatCompletionMessageParam],
    ) -> AsyncGenerator[StandardStreamEvent | CustomStreamEvent, None]:
        """
        Stream events asynchronously.

        Args:
            request: The chat request.
            compiled_state_graph: The compiled state graph.
            messages: The iterable of chat completion message parameters.

        Yields:
            The standard or custom stream event.
        """
        event: StandardStreamEvent | CustomStreamEvent
        async for event in self._stream_graph_with_messages_async(
            request=request,
            compiled_state_graph=compiled_state_graph,
            messages=self.create_messages_for_graph(messages=messages),
        ):
            yield event

    # noinspection PyMethodMayBeStatic
    def create_messages_for_graph(
        self, *, messages: Iterable[ChatCompletionMessageParam]
    ) -> List[tuple[ROLE_TYPES, INCOMING_MESSAGE_TYPES]]:
        """
        Create messages for the graph.

        Args:
            messages: The iterable of chat completion message parameters.

        Returns:
            The list of role and incoming message type tuples.
        """
        return cast(
            List[tuple[ROLE_TYPES, INCOMING_MESSAGE_TYPES]],
            [(m["role"], m["content"]) for m in messages],
        )

    async def run_graph_async(
        self,
        *,
        request: ChatRequest,
        compiled_state_graph: CompiledStateGraph,
    ) -> List[AnyMessage]:
        """
        Run the graph asynchronously.

        Args:
            request: The chat request.
            compiled_state_graph: The compiled state graph.

        Returns:
            The list of any messages.
        """
        messages: List[tuple[ROLE_TYPES, INCOMING_MESSAGE_TYPES]] = (
            self.create_messages_for_graph(messages=request["messages"])
        )

        output_messages: List[AnyMessage] = await self._run_graph_with_messages_async(
            compiled_state_graph=compiled_state_graph, messages=messages
        )
        return output_messages

    # noinspection PyMethodMayBeStatic
    async def create_graph_for_llm_async(
        self, *, llm: BaseChatModel, tools: Sequence[BaseTool]
    ) -> CompiledStateGraph:
        """
        Create a graph for the language model asynchronously.

        Args:
            llm: The base chat model.
            tools: The sequence of tools.

        Returns:
            The compiled state graph.
        """
        if len(tools) > 0:
            return await self._create_graph_for_llm_with_tools_async(
                llm=llm, tools=tools
            )
        else:
            return await self._create_graph_for_llm_without_tools_async(llm=llm)

    # noinspection PyMethodMayBeStatic
    async def _create_graph_for_llm_with_tools_async(
        self, *, llm: BaseChatModel, tools: Sequence[BaseTool]
    ) -> CompiledStateGraph:
        """
        Create a graph for the language model asynchronously.


        :param llm: base chat model
        :param tools: list of tools
        :return: compiled state graph
        """
        tool_node: ToolNode = ToolNode(tools)
        model_with_tools = llm.bind_tools(tools)

        def should_continue(
            state: MyMessagesState,
        ) -> Union[Literal["tools"], str]:
            messages: List[AnyMessage] = state["messages"]
            last_message: AnyMessage = messages[-1]
            # Check if it's an AIMessage and has tool calls
            if isinstance(last_message, AIMessage) and getattr(
                last_message, "tool_calls", None
            ):
                return "tools"
            return END

        async def call_model(state: MyMessagesState) -> MyMessagesState:
            messages: List[AnyMessage] = state["messages"]
            base_message: BaseMessage = await model_with_tools.ainvoke(messages)
            # assert isinstance(base_message, AnyMessage)
            response: AnyMessage = cast(AnyMessage, base_message)
            usage_metadata: Optional[UsageMetadata] = (
                response.usage_metadata if hasattr(response, "usage_metadata") else None
            )
            return MyMessagesState(messages=[response], usage_metadata=usage_metadata)

        workflow = StateGraph(MyMessagesState)

        # Define the two nodes we will cycle between
        workflow.add_node("agent", call_model)  # Now using async call_model
        workflow.add_node("tools", tool_node)

        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", should_continue, ["tools", END])
        workflow.add_edge("tools", "agent")
        workflow.add_edge("agent", END)

        compiled_state_graph: CompiledStateGraph = workflow.compile()
        return compiled_state_graph

    # noinspection PyMethodMayBeStatic
    async def _create_graph_for_llm_without_tools_async(
        self, *, llm: BaseChatModel
    ) -> CompiledStateGraph:
        """
        Create a graph for the language model asynchronously.


        :param llm: base chat model
        :return: compiled state graph
        """

        async def call_model(state: MyMessagesState) -> MyMessagesState:
            messages: List[AnyMessage] = state["messages"]
            base_message: BaseMessage = await llm.ainvoke(messages)
            # assert isinstance(base_message, AnyMessage)
            response: AnyMessage = cast(AnyMessage, base_message)
            usage_metadata: Optional[UsageMetadata] = (
                response.usage_metadata if hasattr(response, "usage_metadata") else None
            )
            return MyMessagesState(messages=[response], usage_metadata=usage_metadata)

        workflow = StateGraph(MyMessagesState)

        # Define the two nodes we will cycle between
        workflow.add_node("agent", call_model)  # Now using async call_model

        workflow.add_edge(START, "agent")
        workflow.add_edge("agent", END)

        compiled_state_graph: CompiledStateGraph = workflow.compile()
        return compiled_state_graph
