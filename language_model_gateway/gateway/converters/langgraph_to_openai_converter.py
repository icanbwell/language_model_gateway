import json
import logging
import os
import time
from typing import (
    Any,
    List,
    Sequence,
    cast,
    Optional,
    Tuple,
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
    ToolMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_core.messages import AIMessageChunk
from langchain_core.messages.ai import UsageMetadata
from langchain_core.runnables.schema import CustomStreamEvent, StandardStreamEvent
from langchain_core.tools import BaseTool
from langgraph.graph.graph import CompiledGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, create_react_agent
from openai import NotGiven, NOT_GIVEN
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
from openai.types.chat.completion_create_params import ResponseFormat
from openai.types.shared_params import ResponseFormatJSONSchema
from openai.types.shared_params.response_format_json_schema import JSONSchema
from starlette.responses import StreamingResponse, JSONResponse

from language_model_gateway.gateway.converters.my_messages_state import MyMessagesState
from language_model_gateway.gateway.converters.streaming_tool_node import (
    StreamingToolNode,
)
from language_model_gateway.gateway.schema.openai.completions import (
    ChatRequest,
    ROLE_TYPES,
    INCOMING_MESSAGE_TYPES,
)
from language_model_gateway.gateway.utilities.chat_message_helpers import (
    langchain_to_chat_message,
    convert_message_content_to_string,
)
from language_model_gateway.gateway.utilities.json_extractor import JsonExtractor

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
        try:
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

                # events are described here: https://python.langchain.com/docs/how_to/streaming/#using-stream-events

                # print(f"===== {event_type} =====\n{event}\n")

                match event_type:
                    case "on_chain_start":
                        # Handle the start of the chain event
                        pass
                    case "on_chain_stream":
                        # Handle the chain stream event.  Be sure not to write duplicate responses to what is done in the on_chat_model_stream event.
                        pass
                    case "on_chat_model_stream":
                        # Handle the chat model stream event
                        chunk: AIMessageChunk | None = event.get("data", {}).get(
                            "chunk"
                        )
                        if chunk is not None:
                            content: str | list[str | dict[str, Any]] = chunk.content

                            # print(f"chunk: {chunk}")

                            usage_metadata = chunk.usage_metadata
                            completion_usage_metadata = (
                                self.convert_usage_meta_data_to_openai(
                                    usages=[usage_metadata] if usage_metadata else []
                                )
                            )

                            content_text: str = convert_message_content_to_string(
                                content
                            )

                            assert isinstance(
                                content_text, str
                            ), f"content_text: {content_text} (type: {type(content_text)})"

                            if (
                                os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1"
                                and content_text
                            ):
                                logger.info(f"Returning content: {content_text}")

                            if content_text:
                                chat_model_stream_response: ChatCompletionChunk = (
                                    ChatCompletionChunk(
                                        id=request_id,
                                        created=int(time.time()),
                                        model=request["model"],
                                        choices=[
                                            ChunkChoice(
                                                index=0,
                                                delta=ChoiceDelta(
                                                    role="assistant",
                                                    content=content_text,
                                                ),
                                            )
                                        ],
                                        usage=completion_usage_metadata,
                                        object="chat.completion.chunk",
                                    )
                                )
                                yield f"data: {json.dumps(chat_model_stream_response.model_dump())}\n\n"
                    case "on_chain_end":
                        # print(f"===== {event_type} =====\n{event}\n")
                        output: Dict[str, Any] | str | None = event.get("data", {}).get(
                            "output"
                        )
                        if (
                            output
                            and isinstance(output, dict)
                            and output.get("usage_metadata")
                        ):
                            completion_usage_metadata = (
                                self.convert_usage_meta_data_to_openai(
                                    usages=[output["usage_metadata"]]
                                )
                            )

                            # Handle the end of the chain event
                            chat_end_stream_response: ChatCompletionChunk = (
                                ChatCompletionChunk(
                                    id=request_id,
                                    created=int(time.time()),
                                    model=request["model"],
                                    choices=[],
                                    usage=completion_usage_metadata,
                                    object="chat.completion.chunk",
                                )
                            )
                            yield f"data: {json.dumps(chat_end_stream_response.model_dump())}\n\n"
                    case "on_tool_start":
                        # Handle the start of the tool event
                        tool_name: Optional[str] = event.get("name", None)
                        tool_input: Dict[str, Any] | None = event.get("data", {}).get(
                            "input"
                        )
                        if tool_name:
                            logger.debug(f"on_tool_start: {tool_name} {tool_input}")
                            chat_stream_response = ChatCompletionChunk(
                                id=request_id,
                                created=int(time.time()),
                                model=request["model"],
                                choices=[
                                    ChunkChoice(
                                        index=0,
                                        delta=ChoiceDelta(
                                            role="assistant",
                                            content=f"\n\n> Running Agent {tool_name}: {tool_input}\n",
                                        ),
                                    )
                                ],
                                usage=CompletionUsage(
                                    prompt_tokens=0,
                                    completion_tokens=0,
                                    total_tokens=0,
                                ),
                                object="chat.completion.chunk",
                            )
                            yield f"data: {json.dumps(chat_stream_response.model_dump())}\n\n"

                    case "on_tool_end":
                        # Handle the end of the tool event
                        tool_message: ToolMessage | None = event.get("data", {}).get(
                            "output"
                        )
                        if tool_message:
                            artifact: Optional[Any] = tool_message.artifact

                            # print(f"on_tool_end: {tool_message}")

                            if artifact:
                                if os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1":
                                    logger.info(f"Returning artifact: {artifact}")

                                chat_stream_response = ChatCompletionChunk(
                                    id=request_id,
                                    created=int(time.time()),
                                    model=request["model"],
                                    choices=[
                                        ChunkChoice(
                                            index=0,
                                            delta=ChoiceDelta(
                                                role="assistant",
                                                content=f"\n> {artifact}\n",
                                            ),
                                        )
                                    ],
                                    usage=CompletionUsage(
                                        prompt_tokens=0,
                                        completion_tokens=0,
                                        total_tokens=0,
                                    ),
                                    object="chat.completion.chunk",
                                )
                                yield f"data: {json.dumps(chat_stream_response.model_dump())}\n\n"
                    case _:
                        # Handle other event types
                        pass
        except Exception as e:
            chat_stream_response = ChatCompletionChunk(
                id=request_id,
                created=int(time.time()),
                model=request["model"],
                choices=[
                    ChunkChoice(
                        index=0,
                        delta=ChoiceDelta(
                            role="assistant",
                            content=f"\nError:\n{e}\n",
                        ),
                    )
                ],
                usage=CompletionUsage(
                    prompt_tokens=0, completion_tokens=0, total_tokens=0
                ),
                object="chat.completion.chunk",
            )
            yield f"data: {json.dumps(chat_stream_response.model_dump())}\n\n"

        yield "data: [DONE]\n\n"

    async def call_agent_with_input(
        self,
        *,
        chat_request: ChatRequest,
        request_id: str,
        compiled_state_graph: CompiledStateGraph,
        system_messages: List[ChatCompletionSystemMessageParam],
    ) -> StreamingResponse | JSONResponse:
        """
        Call the agent with the provided input and return the response.

        Args:
            chat_request: The chat request.
            request_id: The unique request identifier.
            compiled_state_graph: The compiled state graph.
            system_messages: The list of chat completion message parameters.

        Returns:
            The response as a StreamingResponse or JSONResponse.
        """
        assert chat_request is not None
        assert isinstance(chat_request, dict)

        if chat_request.get("stream"):
            return StreamingResponse(
                await self.get_streaming_response_async(
                    request=chat_request,
                    request_id=request_id,
                    compiled_state_graph=compiled_state_graph,
                    system_messages=system_messages,
                ),
                media_type="text/event-stream",
            )
        else:
            try:
                json_output_requested: bool
                chat_request, json_output_requested = self.add_system_messages_for_json(
                    chat_request=chat_request
                )

                responses: List[AnyMessage] = await self.ainvoke(
                    compiled_state_graph=compiled_state_graph,
                    request=chat_request,
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

                choices_text = "\n".join([f"{c.message.content}" for c in choices])

                if json_output_requested:
                    # extract the json content from response and just return that
                    json_content_raw: Dict[str, Any] | List[Dict[str, Any]] | str = (
                        (JsonExtractor.extract_structured_output(text=choices_text))
                        if choices_text
                        else choices_text
                    )
                    json_content: str = json.dumps(json_content_raw)
                    choices = [
                        Choice(
                            index=i,
                            message=ChatCompletionMessage(
                                content=json_content, role="assistant"
                            ),
                            finish_reason="stop",
                        )
                        for i in range(1)
                    ]

                if os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1" and choices_text:
                    logger.info(f"Returning content: {choices_text}")

                chat_response: ChatCompletion = ChatCompletion(
                    id=request_id,
                    model=chat_request["model"],
                    choices=choices,
                    usage=total_usage_metadata,
                    created=int(time.time()),
                    object="chat.completion",
                )
                return JSONResponse(content=chat_response.model_dump())
            except Exception as e:
                logger.exception(e, stack_info=True)
                raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    @staticmethod
    def add_system_messages_for_json(
        *, chat_request: ChatRequest
    ) -> Tuple[ChatRequest, bool]:
        """
        If the user is requesting json_object or json_schema output, add system messages to the chat request
        to generate JSON output.


        :param chat_request:
        :return:
        """
        json_response_requested: bool = False
        response_format: ResponseFormat | NotGiven = chat_request.get(
            "response_format", NOT_GIVEN
        )
        if isinstance(response_format, NotGiven):
            return chat_request, json_response_requested

        match response_format.get("type", None):
            case "text":
                return chat_request, json_response_requested
            case "json_object":
                json_response_requested = True
                json_object_system_message_text: str = """                
                Respond only with a JSON object or array.
                
                Output follows this example format:
                <json>
                json  here
                </json>"""
                json_object_system_message: ChatCompletionSystemMessageParam = (
                    ChatCompletionSystemMessageParam(
                        role="system", content=json_object_system_message_text
                    )
                )
                chat_request["messages"] = [r for r in chat_request["messages"]] + [
                    json_object_system_message
                ]
                return chat_request, json_response_requested
            case "json_schema":
                json_response_requested = True
                json_response_format: ResponseFormatJSONSchema = cast(
                    ResponseFormatJSONSchema,
                    response_format,
                )
                json_schema: JSONSchema | None = json_response_format.get("json_schema")
                assert (
                    json_schema is not None
                ), "json_schema should be specified in response_format if type is json_schema"
                json_schema_system_message_text: str = f"""                
                Respond only with a JSON object or array using the provided schema:
                ```{json_schema}``` 
    
                Output follows this example format:
                <json>
                json  here
                </json>"""
                json_schema_system_message: ChatCompletionSystemMessageParam = (
                    ChatCompletionSystemMessageParam(
                        role="system", content=json_schema_system_message_text
                    )
                )
                chat_request["messages"] = [r for r in chat_request["messages"]] + [
                    json_schema_system_message
                ]
                return chat_request, json_response_requested
            case _:
                raise ValueError(
                    f"Unexpected response format type: {response_format.get('type', None)}"
                )

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
        chat_request: ChatRequest,
        messages: List[BaseMessage],
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

        output: Dict[str, Any] = await compiled_state_graph.ainvoke(
            input=self.create_state(chat_request=chat_request, messages=messages)
        )
        out_messages: List[AnyMessage] = output["messages"]
        return out_messages

    # noinspection PyMethodMayBeStatic
    async def _stream_graph_with_messages_async(
        self,
        *,
        request: ChatRequest,
        messages: List[BaseMessage],
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

        event: StandardStreamEvent | CustomStreamEvent
        async for event in compiled_state_graph.astream_events(
            input=self.create_state(chat_request=request, messages=messages),
            version="v2",
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
            chat_request=request,
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
    ) -> List[BaseMessage]:
        """
        Create messages for the graph.

        Args:
            messages: The iterable of chat completion message parameters.

        Returns:
            The list of role and incoming message type tuples.
        """
        chat_messages: List[tuple[ROLE_TYPES, INCOMING_MESSAGE_TYPES]] = cast(
            List[tuple[ROLE_TYPES, INCOMING_MESSAGE_TYPES]],
            [(m["role"], m["content"]) for m in messages],
        )

        messages_: List[BaseMessage] = []
        for role, content in chat_messages:
            match role:
                case "system":
                    messages_.append(
                        SystemMessage(
                            content=self.convert_incoming_message_content_to_string(
                                content
                            ),
                            role="system",
                        )
                    )
                case "user":
                    messages_.append(
                        HumanMessage(
                            content=self.convert_incoming_message_content_to_string(
                                content
                            ),
                            role="user",
                        )
                    )
                case "assistant":
                    messages_.append(
                        AIMessage(
                            content=self.convert_incoming_message_content_to_string(
                                content
                            ),
                            role="assistant",
                        )
                    )
                case "tool":
                    messages_.append(
                        ToolMessage(
                            content=self.convert_incoming_message_content_to_string(
                                content
                            ),
                            role="tool",
                        )
                    )
                case _:
                    raise ValueError(f"Unexpected role: {role}")

        return messages_

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
        messages: List[BaseMessage] = self.create_messages_for_graph(
            messages=request["messages"]
        )

        output_messages: List[AnyMessage] = await self._run_graph_with_messages_async(
            chat_request=request,
            compiled_state_graph=compiled_state_graph,
            messages=messages,
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
        return await self._create_graph_for_llm_with_tools_async(llm=llm, tools=tools)

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
        tool_node: ToolNode | None = None
        if len(tools) > 0:
            tool_node = StreamingToolNode(tools)

        compiled_state_graph: CompiledGraph = create_react_agent(
            model=llm,
            tools=tool_node if tool_node is not None else [],
            state_schema=MyMessagesState,
        )
        return cast(CompiledStateGraph, compiled_state_graph)

    @staticmethod
    def add_completion_usage(
        *, original: CompletionUsage, new_one: CompletionUsage
    ) -> CompletionUsage:
        """
        Add completion usage metadata.

        Args:
            original: The original completion usage metadata.
            new_one: The new completion usage metadata.

        Returns:
            The completion usage metadata.
        """
        return CompletionUsage(
            prompt_tokens=original.prompt_tokens + new_one.prompt_tokens,
            completion_tokens=original.completion_tokens + new_one.completion_tokens,
            total_tokens=original.total_tokens + new_one.total_tokens,
        )

    @staticmethod
    def create_state(
        *, chat_request: ChatRequest, messages: List[BaseMessage]
    ) -> MyMessagesState:
        input1: MyMessagesState = MyMessagesState(
            messages=messages,
            auth_token="foo",
            is_last_step=False,
            usage_metadata=None,
            remaining_steps=0,
            structured_response={},
        )
        return input1

    @staticmethod
    def convert_incoming_message_content_to_string(
        content_: INCOMING_MESSAGE_TYPES,
    ) -> str:
        """
        Convert the message content to a string.

        Args:
            content_: The message content.

        Returns:
            The message content as a string.
        """
        text: List[str] = []
        if isinstance(content_, str):
            text.append(content_)
        elif isinstance(content_, list):
            for content_item in content_:
                content_item_type: Optional[str] = content_item.get("type")
                if content_item_type == "text":
                    text.append(content_item.get("text") or "")
                else:
                    raise ValueError(
                        f"Unsupported content item type: {type(content_item)}: {content_item}"
                    )
        return "".join(text)
