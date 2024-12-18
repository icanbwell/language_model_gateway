from typing import Optional, List

import httpx
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from language_model_gateway.configs.config_schema import (
    ChatModelConfig,
    ModelConfig,
    ToolConfig,
)
from language_model_gateway.container.simple_container import SimpleContainer
from language_model_gateway.gateway.api_container import get_container_async
from language_model_gateway.gateway.models.model_factory import ModelFactory
from language_model_gateway.gateway.utilities.environment_reader import (
    EnvironmentReader,
)
from language_model_gateway.gateway.utilities.expiring_cache import ExpiringCache
from tests.gateway.mocks.mock_chat_model import MockChatModel
from tests.gateway.mocks.mock_model_factory import MockModelFactory


async def test_chat_open_ai(async_client: httpx.AsyncClient) -> None:
    print("")

    test_container: SimpleContainer = await get_container_async()
    if not EnvironmentReader.is_environment_variable_set("RUN_TESTS_WITH_REAL_LLM"):
        test_container.register(
            ModelFactory,
            lambda c: MockModelFactory(
                fn_get_model=lambda chat_model_config: MockChatModel(
                    fn_get_response=lambda messages: "Barack"
                )
            ),
        )

    # set the model configuration for this test
    model_configuration_cache: ExpiringCache[List[ChatModelConfig]] = (
        test_container.resolve(ExpiringCache)
    )
    await model_configuration_cache.set(
        [
            ChatModelConfig(
                id="chat_gpt",
                name="ChatGPT",
                description="General Purpose Language Model",
                type="langchain",
                model=ModelConfig(
                    provider="openai",
                    model="gpt-4o",
                ),
                tools=[
                    ToolConfig(name="image_generator_openai"),
                ],
            )
        ]
    )
    # Test health endpoint
    # response = await async_client.get("/health")
    # assert response.status_code == 200

    # init client and connect to localhost server
    client = AsyncOpenAI(
        api_key="fake-api-key",
        base_url="http://localhost:5000/api/v1",  # change the default port if needed
        http_client=async_client,
    )

    # call API
    chat_completion: ChatCompletion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "what is the first name of Obama?",
            }
        ],
        model="ChatGPT",
    )

    # print the top "choice"
    content: Optional[str] = "\n".join(
        choice.message.content or "" for choice in chat_completion.choices
    )

    assert content is not None
    print(content)
    assert "Barack" in content


async def test_chat_completions_with_chat_history(
    async_client: httpx.AsyncClient,
) -> None:
    print("")

    test_container: SimpleContainer = await get_container_async()
    if not EnvironmentReader.is_environment_variable_set("RUN_TESTS_WITH_REAL_LLM"):
        test_container.register(
            ModelFactory,
            lambda c: MockModelFactory(
                fn_get_model=lambda chat_model_config: MockChatModel(
                    fn_get_response=lambda messages: "Barack"
                )
            ),
        )

    # set the model configuration for this test
    model_configuration_cache: ExpiringCache[List[ChatModelConfig]] = (
        test_container.resolve(ExpiringCache)
    )
    await model_configuration_cache.set(
        [
            ChatModelConfig(
                id="chat_gpt",
                name="ChatGPT",
                description="General Purpose Language Model",
                type="langchain",
                model=ModelConfig(
                    provider="openai",
                    model="gpt-4o",
                ),
                tools=[
                    ToolConfig(name="image_generator_openai"),
                ],
            )
        ]
    )

    # init client and connect to localhost server
    client = AsyncOpenAI(
        api_key="fake-api-key",
        base_url="http://localhost:5000/api/v1",  # change the default port if needed
        http_client=async_client,
    )

    # call API
    chat_completion: ChatCompletion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Who was the 44th president of United States? ",
            },
            {"role": "assistant", "content": "Barack Obama"},
            {
                "role": "user",
                "content": "what is his first name?",
            },
        ],
        model="ChatGPT",
    )

    # print the top "choice"
    print("========  Response ======")
    print(chat_completion)
    print("====== End of Response ======")
    content: Optional[str] = "\n".join(
        choice.message.content or "" for choice in chat_completion.choices
    )
    assert content is not None
    print(content)
    assert "Barack" in content
