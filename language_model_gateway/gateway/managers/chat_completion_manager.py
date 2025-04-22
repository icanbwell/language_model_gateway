import json
import logging
import os
import time
from typing import Dict, List, cast, AsyncGenerator, Optional

from fastapi import HTTPException
from openai.types import CompletionUsage
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionMessageParam,
    ChatCompletion,
    ChatCompletionMessage,
    ChatCompletionUserMessageParam,
    ChatCompletionChunk,
)
from openai.types.chat.chat_completion import Choice
from starlette.responses import StreamingResponse, JSONResponse

from language_model_gateway.configs.config_reader.config_reader import ConfigReader
from language_model_gateway.configs.config_schema import ChatModelConfig, PromptConfig
from language_model_gateway.gateway.providers.base_chat_completions_provider import (
    BaseChatCompletionsProvider,
)
from language_model_gateway.gateway.providers.langchain_chat_completions_provider import (
    LangChainCompletionsProvider,
)
from language_model_gateway.gateway.providers.openai_chat_completions_provider import (
    OpenAiChatCompletionsProvider,
)
from language_model_gateway.gateway.schema.openai.completions import ChatRequest
from openai.types.chat.chat_completion_chunk import ChoiceDelta, Choice as ChunkChoice

logger = logging.getLogger(__name__)


class ChatCompletionManager:
    """
    Implements the chat completion manager following the OpenAI API
    https://platform.openai.com/docs/overview
    https://github.com/openai/openai-python/blob/main/api.md


    """

    def __init__(
        self,
        *,
        open_ai_provider: OpenAiChatCompletionsProvider,
        langchain_provider: LangChainCompletionsProvider,
        config_reader: ConfigReader,
    ) -> None:
        """
        Chat completion manager

        :param open_ai_provider: provider to use for OpenAI completions
        :param langchain_provider: provider to use for LangChain completions
        :return:
        """

        self.openai_provider: OpenAiChatCompletionsProvider = open_ai_provider
        assert self.openai_provider is not None
        assert isinstance(self.openai_provider, OpenAiChatCompletionsProvider)
        self.langchain_provider: LangChainCompletionsProvider = langchain_provider
        assert self.langchain_provider is not None
        assert isinstance(self.langchain_provider, LangChainCompletionsProvider)
        self.config_reader: ConfigReader = config_reader
        assert self.config_reader is not None
        assert isinstance(self.config_reader, ConfigReader)

    # noinspection PyMethodMayBeStatic
    async def chat_completions(
        self,
        *,
        headers: Dict[str, str],
        chat_request: ChatRequest,
    ) -> StreamingResponse | JSONResponse:
        # Use the model to choose the provider
        try:
            model: str = chat_request["model"]
            assert model is not None

            configs: List[
                ChatModelConfig
            ] = await self.config_reader.read_model_configs_async()

            # Find the model config
            model_config: ChatModelConfig | None = next(
                (config for config in configs if config.name.lower() == model.lower()),
                None,
            )
            if model_config is None:
                logger.error(f"Model {model} not found in the config")
                raise HTTPException(
                    status_code=400, detail=f"Model {model} not found in the config"
                )

            chat_request = self.add_system_messages(
                chat_request=chat_request, system_prompts=model_config.system_prompts
            )

            provider: BaseChatCompletionsProvider
            match model_config.type:
                case "openai":
                    provider = self.openai_provider
                case "langchain":
                    provider = self.langchain_provider
                case _:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Model type {model_config.type} not supported",
                    )

            help_response: StreamingResponse | JSONResponse | None = (
                self.handle_help_prompt(
                    chat_request=chat_request, model=model, model_config=model_config
                )
            )
            if help_response is not None:
                return help_response

            if os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1":
                logger.info(
                    f"Running chat completion for {chat_request} with headers {headers}"
                )
            # Use the provider to get the completions
            response: (
                StreamingResponse | JSONResponse
            ) = await provider.chat_completions(
                model_config=model_config,
                headers=headers,
                chat_request=chat_request,
            )
            return response
        except Exception as e:
            return await self.handle_exception(chat_request=chat_request, e=e)

    # noinspection PyMethodMayBeStatic
    def add_system_messages(
        self, chat_request: ChatRequest, system_prompts: List[PromptConfig] | None
    ) -> ChatRequest:
        # see if there are any system prompts in chat_request
        has_system_messages_in_chat_request: bool = any(
            [
                message
                for message in chat_request["messages"]
                if message["role"] == "system"
            ]
        )
        if (
            not has_system_messages_in_chat_request
            and system_prompts is not None
            and len(system_prompts) > 0
        ):
            system_messages: List[ChatCompletionSystemMessageParam] = [
                ChatCompletionSystemMessageParam(role="system", content=message.content)
                for message in system_prompts
                if message.role == "system" and message.content is not None
            ]
            chat_request["messages"] = system_messages + [
                r for r in chat_request["messages"]
            ]

        return chat_request

    # noinspection PyMethodMayBeStatic
    def handle_help_prompt(
        self, *, chat_request: ChatRequest, model: str, model_config: ChatModelConfig
    ) -> StreamingResponse | JSONResponse | None:
        request_messages: List[ChatCompletionMessageParam] = [
            m for m in chat_request["messages"]
        ]
        if request_messages is None:
            logger.error("Messages not found in the request")
            raise HTTPException(
                status_code=400, detail="Messages not found in the request"
            )

        user_messages: List[ChatCompletionUserMessageParam] = [
            m for m in request_messages if m["role"] == "user"
        ]
        if user_messages is None or len(user_messages) == 0:
            logger.error("User messages not found in the request")
            raise HTTPException(
                status_code=400, detail="User messages not found in the request"
            )

        last_message_content: str = cast(str, user_messages[-1]["content"])
        if os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1":
            logger.info(
                f"Last message content: {last_message_content}, type: {type(last_message_content)}"
            )

        help_keywords: List[str] = os.environ.get("HELP_KEYWORDS", "help").split(";")
        if (
            isinstance(last_message_content, str)
            and last_message_content.lower() in help_keywords
        ):
            logger.info(f"Help requested for model {model}")
            response_messages: List[ChatCompletionMessage] = [
                ChatCompletionMessage(
                    role="assistant",
                    content=model_config.description or "No description available",
                )
            ]
            if model_config.owner is not None:
                response_messages.append(
                    ChatCompletionMessage(
                        role="assistant", content=f"Model owner: {model_config.owner}"
                    )
                )
            if model_config.example_prompts is not None:
                response_messages.append(
                    ChatCompletionMessage(
                        role="assistant", content="Here are some example prompts:"
                    )
                )
                response_messages.extend(
                    [
                        ChatCompletionMessage(role="assistant", content=prompt.content)
                        for prompt in model_config.example_prompts
                    ]
                )

            return self.write_response(
                chat_request=chat_request, response_messages=response_messages
            )

        return None

    # noinspection PyMethodMayBeStatic
    def write_response(
        self,
        *,
        chat_request: ChatRequest,
        response_messages: List[ChatCompletionMessage],
    ) -> StreamingResponse | JSONResponse:
        chat_model: str = chat_request["model"]
        should_stream_response: Optional[bool] = cast(
            Optional[bool], chat_request.get("stream")
        )
        if should_stream_response:

            async def foo(
                response_messages1: List[ChatCompletionMessage],
            ) -> AsyncGenerator[str, None]:
                for response_message in response_messages1:
                    if response_message.content:
                        chat_stream_response: ChatCompletionChunk = ChatCompletionChunk(
                            id="1",
                            created=int(time.time()),
                            model=chat_model,
                            choices=[
                                ChunkChoice(
                                    index=0,
                                    delta=ChoiceDelta(
                                        role="assistant",
                                        content=response_message.content + "\n",
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
                yield "data: [DONE]\n\n"

            return StreamingResponse(
                content=foo(response_messages1=response_messages),
                media_type="text/event-stream",
            )
        else:
            choices: List[Choice] = [
                Choice(index=i, message=m, finish_reason="stop")
                for i, m in enumerate(response_messages)
            ]
            chat_response: ChatCompletion = ChatCompletion(
                id="1",
                model=chat_model,
                choices=choices,
                usage=CompletionUsage(
                    prompt_tokens=0,
                    completion_tokens=0,
                    total_tokens=0,
                ),
                created=int(time.time()),
                object="chat.completion",
            )
            if os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1":
                logger.info(f"Returning help response: {chat_response.model_dump()}")

            return JSONResponse(content=chat_response.model_dump())

    async def handle_exception(
        self, *, chat_request: ChatRequest, e: Exception
    ) -> StreamingResponse | JSONResponse:
        logger.error(f"Error in chat completion: {e}")
        return self.write_response(
            chat_request=chat_request,
            response_messages=[ChatCompletionMessage(role="assistant", content=str(e))],
        )
