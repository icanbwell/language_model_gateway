import json
import logging
import random
import time
from os import environ
from typing import AsyncGenerator, cast, List, Any, Dict, Optional

import httpx
from httpx import Response
from starlette.responses import StreamingResponse, JSONResponse

from language_model_gateway.gateway.schema import (
    ChatResponseMessage,
    ChatResponse,
    Choice,
    Usage,
    ChoiceDelta,
    ChatStreamResponse,
    UserMessage,
    ChatRequest,
    SystemMessage,
    AssistantMessage,
    ToolMessage,
)
from httpx_sse import aconnect_sse, ServerSentEvent

logger = logging.getLogger(__file__)


class ChatCompletionsManager:

    @staticmethod
    async def _resp_async_generator(
        *, request_model: str, text_resp: str
    ) -> AsyncGenerator[str, None]:
        tokens = text_resp.split(" ")
        for i, token in enumerate(tokens):
            chunk: ChatStreamResponse = ChatStreamResponse(
                id=str(i),
                created=int(time.time()),
                model=request_model,
                choices=[
                    ChoiceDelta(
                        delta=ChatResponseMessage(role="assistant", content=token + " ")
                    )
                ],
                usage=Usage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
            )
            yield f"data: {json.dumps(chunk.model_dump())}\n\n"
        yield "data: [DONE]\n\n"

    @staticmethod
    async def _stream_resp_async_generator(
        *,
        request_id: str,
        agent_url: str,
        test_data: Dict[str, Any],
        request_model: str,
    ) -> AsyncGenerator[str, None]:

        logger.info(f"Streaming response {request_id} from agent")
        async with httpx.AsyncClient(base_url=agent_url) as client:
            async with aconnect_sse(
                client,
                "POST",
                "/stream",
                json={"input": test_data},
                timeout=60 * 60,
            ) as event_source:
                i = 0
                sse: ServerSentEvent
                async for sse in event_source.aiter_sse():
                    event: str = sse.event
                    data: str = sse.data
                    i += 1

                    logger.info(f"----- Received data from stream {i} {event} ------")
                    logger.info(data)
                    logger.info(f"----- End data from stream {i} {event} ------")
                    chunk: ChatStreamResponse = ChatStreamResponse(
                        id=str(i),
                        created=int(time.time()),
                        model=request_model,
                        choices=[
                            ChoiceDelta(
                                delta=ChatResponseMessage(
                                    role="assistant", content=data
                                )
                            )
                        ],
                        usage=Usage(
                            prompt_tokens=0, completion_tokens=0, total_tokens=0
                        ),
                    )
                    yield f"data: {json.dumps(chunk.model_dump())}\n\n"
                yield "data: [DONE]\n\n"

    async def chat_completions(
        self,
        *,
        request: ChatRequest,
    ) -> StreamingResponse | JSONResponse:
        request_id = random.randint(1, 1000)
        logger.info(f"Received request {request_id}: {request}")

        response_context: str
        if request.messages:
            resp_content = cast(str, cast(UserMessage, request.messages[-1]).content)
        else:
            resp_content = "As a mock AI Assistant, I can only echo your last message, but there wasn't one!"

        if resp_content == "dummy":
            if request.stream:
                logger.info(f"Streaming response {request_id}")
                return StreamingResponse(
                    ChatCompletionsManager._resp_async_generator(
                        request_model=request.model, text_resp=resp_content
                    ),
                    media_type="text/event-stream",
                )
            response_dict: ChatResponse = ChatResponse(
                id="1337",
                created=int(time.time()),
                model=request.model,
                choices=[
                    Choice(
                        message=ChatResponseMessage(
                            role="assistant", content=resp_content
                        )
                    )
                ],
                usage=Usage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
            )
            logger.info(f"Non-streaming response {request_id}: {response_dict}")
            return JSONResponse(content=response_dict.model_dump())
        else:
            return await self.call_ai_agent(request=request, request_id=str(request_id))

    async def call_ai_agent(
        self, *, request: ChatRequest, request_id: str
    ) -> StreamingResponse | JSONResponse:
        input_text: str = cast(str, cast(UserMessage, request.messages[-1]).content)
        chat_history: List[
            SystemMessage | UserMessage | AssistantMessage | ToolMessage
        ] = request.messages
        return await self.call_agent_with_input(
            chat_history=[c.model_dump() for c in chat_history],
            input_text=input_text,
            model=request.model,
            agent_url=environ["AGENT_URL"],
            patient_id=environ["DEFAULT_PATIENT_ID"],
            request_id=request_id,
            stream_request=request.stream,
        )

    @staticmethod
    async def call_agent_with_input(
        *,
        chat_history: List[Dict[str, Any]],
        input_text: str,
        model: str,
        agent_url: str,
        patient_id: str,
        request_id: str,
        stream_request: Optional[bool],
    ) -> StreamingResponse | JSONResponse:
        assert agent_url
        assert patient_id
        assert input_text
        assert isinstance(chat_history, list)

        test_data = {
            "input": input_text,
            "patient_id": patient_id,
            "chat_history": chat_history,
        }
        if stream_request:
            return StreamingResponse(
                await ChatCompletionsManager.get_streaming_response_async(
                    model=model,
                    agent_url=agent_url,
                    request_id=request_id,
                    test_data=test_data,
                ),
                media_type="text/event-stream",
            )

        async with httpx.AsyncClient(base_url=agent_url) as client:
            agent_response: Response = await client.post(
                "/invoke", json={"input": test_data}, timeout=60 * 60
            )

            response_text: str = agent_response.text
            try:
                response_dict: Dict[str, Any] = agent_response.json()
            except json.JSONDecodeError:
                response_dict = {
                    "output": {
                        "output": [
                            {"text": f"{agent_response.status_code} {response_text}"},
                        ]
                    }
                }

            assert agent_response.status_code == 200
            assert "output" in response_dict
            output_dict: Dict[str, Any] = response_dict["output"]
            outputs: List[Dict[str, Any]] = output_dict["output"]
            assert len(outputs) == 1
            output_text: str = outputs[0]["text"]

            response: ChatResponse = ChatResponse(
                id="1337",
                created=int(time.time()),
                model=model,
                choices=[
                    Choice(
                        message=ChatResponseMessage(
                            role="assistant", content=output_text
                        )
                    )
                ],
                usage=Usage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
            )
            logger.info(f"Non-streaming response {request_id}: {response}")
            return JSONResponse(content=response.model_dump())

    @staticmethod
    async def get_streaming_response_async(
        *, agent_url: str, model: str, request_id: str, test_data: Dict[str, Any]
    ) -> AsyncGenerator[str, None]:
        logger.info(f"Streaming response {request_id} from agent")
        generator: AsyncGenerator[str, None] = (
            ChatCompletionsManager._stream_resp_async_generator(
                request_model=model,
                agent_url=agent_url,
                test_data=test_data,
                request_id=request_id,
            )
        )
        return generator
