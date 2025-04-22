from typing import Optional
import json
import logging
import os
from os import environ
from random import randint
from typing import Any, Dict, AsyncGenerator

from httpx import Response
from httpx_sse import aconnect_sse, ServerSentEvent
from openai.types.chat import (
    ChatCompletion,
)
from pydantic_core import ValidationError

from language_model_gateway.configs.config_schema import ChatModelConfig
from language_model_gateway.gateway.http.http_client_factory import HttpClientFactory


from starlette.responses import StreamingResponse, JSONResponse

from language_model_gateway.gateway.providers.base_chat_completions_provider import (
    BaseChatCompletionsProvider,
)
from language_model_gateway.gateway.schema.openai.completions import ChatRequest

logger = logging.getLogger(__file__)


class OpenAiChatCompletionsProvider(BaseChatCompletionsProvider):
    def __init__(self, *, http_client_factory: HttpClientFactory) -> None:
        self.http_client_factory: HttpClientFactory = http_client_factory
        assert self.http_client_factory is not None
        assert isinstance(self.http_client_factory, HttpClientFactory)

    async def chat_completions(
        self,
        *,
        model_config: ChatModelConfig,
        headers: Dict[str, str],
        chat_request: ChatRequest,
    ) -> StreamingResponse | JSONResponse:
        """
        Call the OpenAI API to get chat completions

        :param headers:
        :param chat_request:
        :param model_config:
        :return:
        """
        assert chat_request

        request_id: str = str(randint(1, 1000))
        agent_url: Optional[str] = model_config.url or environ["OPENAI_AGENT_URL"]
        assert agent_url

        if chat_request.get("stream"):
            return StreamingResponse(
                await self.get_streaming_response_async(
                    agent_url=agent_url,
                    request_id=request_id,
                    headers=headers,
                    chat_request=chat_request,
                ),
                media_type="text/event-stream",
            )

        response_text: Optional[str] = None
        async with self.http_client_factory.create_http_client(
            base_url="http://test"
        ) as client:
            try:
                agent_response: Response = await client.post(
                    agent_url,
                    json=chat_request,
                    timeout=60 * 60,
                    headers=headers,
                )

                response_text = agent_response.text
                response_dict: Dict[str, Any] = agent_response.json()
            except json.JSONDecodeError:
                return JSONResponse(
                    content=f"Error decoding response. url: {agent_url}\n{response_text}",
                    status_code=500,
                )
            except Exception as e:
                return JSONResponse(
                    content=f"Error from agent: {e} url: {agent_url}\n{response_text}",
                    status_code=500,
                )

            try:
                response: ChatCompletion = ChatCompletion.model_validate(response_dict)
            except ValidationError as e:
                return JSONResponse(
                    content=f"Error validating response: {e}. url: {agent_url}\n{response_text}",
                    status_code=500,
                )
            if os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1":
                logger.info(f"Non-streaming response {request_id}: {response}")
            return JSONResponse(content=response.model_dump())

    async def get_streaming_response_async(
        self,
        *,
        agent_url: str,
        request_id: str,
        headers: Dict[str, str],
        chat_request: ChatRequest,
    ) -> AsyncGenerator[str, None]:
        logger.info(f"Streaming response {request_id} from agent")
        generator: AsyncGenerator[str, None] = self._stream_resp_async_generator(
            agent_url=agent_url,
            request_id=request_id,
            chat_request=chat_request,
            headers=headers,
        )
        return generator

    async def _stream_resp_async_generator(
        self,
        *,
        request_id: str,
        agent_url: str,
        chat_request: ChatRequest,
        headers: Dict[str, str],
    ) -> AsyncGenerator[str, None]:
        logger.info(f"Streaming response {request_id} from agent")
        async with self.http_client_factory.create_http_client(
            base_url="http://test"
        ) as client:
            async with aconnect_sse(
                client,
                "POST",
                agent_url,
                json=chat_request,
                timeout=60 * 60,
                headers=headers,
            ) as event_source:
                i = 0
                sse: ServerSentEvent
                async for sse in event_source.aiter_sse():
                    event: str = sse.event
                    data: str = sse.data
                    i += 1

                    if os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1":
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug(
                                f"----- Received data from stream {i} {event} {type(data)} ------"
                            )
                            logger.debug(data)
                            logger.debug(
                                f"----- End data from stream {i} {event} {type(data)} ------"
                            )
                    yield f"data: {data}\n\n"
