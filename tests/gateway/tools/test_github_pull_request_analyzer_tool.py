from typing import Optional, List

import httpx
from openai import AsyncOpenAI, AsyncStream
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai.types.chat.chat_completion import Choice

from language_model_gateway.configs.config_schema import (
    ChatModelConfig,
    ModelConfig,
    AgentConfig,
)
from language_model_gateway.container.simple_container import SimpleContainer
from language_model_gateway.gateway.api_container import get_container_async
from language_model_gateway.gateway.image_generation.image_generator_factory import (
    ImageGeneratorFactory,
)
from language_model_gateway.gateway.models.model_factory import ModelFactory
from language_model_gateway.gateway.utilities.environment_reader import (
    EnvironmentReader,
)
from language_model_gateway.gateway.utilities.environment_variables import (
    EnvironmentVariables,
)
from language_model_gateway.gateway.utilities.expiring_cache import ExpiringCache
from tests.gateway.mocks.mock_chat_model import MockChatModel
from tests.gateway.mocks.mock_environment_variables import MockEnvironmentVariables
from tests.gateway.mocks.mock_image_generator import MockImageGenerator
from tests.gateway.mocks.mock_image_generator_factory import MockImageGeneratorFactory
from tests.gateway.mocks.mock_model_factory import MockModelFactory


async def test_github_pull_request_analyzer_tool(
    async_client: httpx.AsyncClient,
) -> None:
    print("")

    test_container: SimpleContainer = await get_container_async()

    if not EnvironmentReader.is_environment_variable_set("RUN_TESTS_WITH_REAL_LLM"):
        test_container.register(
            EnvironmentVariables, lambda c: MockEnvironmentVariables()
        )

        test_container.register(
            ModelFactory,
            lambda c: MockModelFactory(
                fn_get_model=lambda chat_model_config: MockChatModel(
                    fn_get_response=lambda messages: "helix.pipelines"
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
                id="general_purpose",
                name="General Purpose",
                description="General Purpose Language Model",
                type="langchain",
                model=ModelConfig(
                    provider="bedrock",
                    model="us.anthropic.claude-3-5-haiku-20241022-v1:0",
                ),
                tools=[
                    AgentConfig(name="current_date"),
                    AgentConfig(name="github_pull_request_analyzer"),
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
        default_headers={"Authorization": "Bearer fake-api-key"},
    )

    # call API
    chat_completion: ChatCompletion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Get the pull requests per contributor for the helix.pipelines repository for past 3 months",
            }
        ],
        model="General Purpose",
    )

    print(chat_completion)

    # print the top "choice"
    choices: List[Choice] = chat_completion.choices
    print(choices)
    content: Optional[str] = ",".join(
        [choice.message.content or "" for choice in choices]
    )
    assert content is not None
    print("======== Final Content ========")
    print(content)
    print("====== End of Final Content ======")
    assert "helix.pipelines" in content


async def test_github_pull_request_analyzer_tool_streaming(
    async_client: httpx.AsyncClient,
) -> None:
    print("")
    test_container: SimpleContainer = await get_container_async()

    if not EnvironmentReader.is_environment_variable_set("RUN_TESTS_WITH_REAL_LLM"):
        test_container.register(
            EnvironmentVariables, lambda c: MockEnvironmentVariables()
        )
        test_container.register(
            ModelFactory,
            lambda c: MockModelFactory(
                fn_get_model=lambda chat_model_config: MockChatModel(
                    fn_get_response=lambda messages: "helix.pipelines"
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
                id="general_purpose",
                name="General Purpose",
                description="General Purpose Language Model",
                type="langchain",
                model=ModelConfig(
                    provider="bedrock",
                    model="us.anthropic.claude-3-5-haiku-20241022-v1:0",
                ),
                tools=[
                    AgentConfig(name="current_date"),
                    AgentConfig(name="github_pull_request_analyzer"),
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
        default_headers={"Authorization": "Bearer fake-api-key"},
    )

    # call API
    stream: AsyncStream[ChatCompletionChunk] = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Get the pull requests per contributor for the helix.pipelines repository for past 3 months",
            }
        ],
        model="General Purpose",
        stream=True,
    )

    content: Optional[str] = None
    chunk: ChatCompletionChunk
    async for chunk in stream:
        delta_content = "\n".join(
            [choice.delta.content or "" for choice in chunk.choices]
        )
        if delta_content:
            print("======= Chunk =======")
            print(delta_content)
            print("======= End of Chunk =======")
            content = content + delta_content if content else delta_content

    assert content is not None
    print(content)
    assert content is not None
    print("======== Final Content ========")
    print(content)
    print("====== End of Final Content ======")
    assert "helix.pipelines" in content


async def test_github_pull_request_analyzer_full_details_tool(
    async_client: httpx.AsyncClient,
) -> None:
    print("")
    test_container: SimpleContainer = await get_container_async()

    if not EnvironmentReader.is_environment_variable_set("RUN_TESTS_WITH_REAL_LLM"):
        test_container.register(
            ModelFactory,
            lambda c: MockModelFactory(
                fn_get_model=lambda chat_model_config: MockChatModel(
                    fn_get_response=lambda messages: "helix.pipelines"
                )
            ),
        )
        test_container.register(
            ImageGeneratorFactory,
            lambda c: MockImageGeneratorFactory(image_generator=MockImageGenerator()),
        )

    # set the model configuration for this test
    model_configuration_cache: ExpiringCache[List[ChatModelConfig]] = (
        test_container.resolve(ExpiringCache)
    )
    await model_configuration_cache.set(
        [
            ChatModelConfig(
                id="general_purpose",
                name="General Purpose",
                description="General Purpose Language Model",
                type="langchain",
                model=ModelConfig(
                    provider="bedrock",
                    model="us.anthropic.claude-3-5-haiku-20241022-v1:0",
                ),
                tools=[
                    AgentConfig(name="current_date"),
                    AgentConfig(name="github_pull_request_analyzer"),
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
        default_headers={"Authorization": "Bearer fake-api-key"},
    )

    # call API
    chat_completion: ChatCompletion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "List all the pull requests with title, author and description for the helix.pipelines repository for past 3 months",
            }
        ],
        model="General Purpose",
    )

    print(chat_completion)

    # print the top "choice"
    choices: List[Choice] = chat_completion.choices
    print(choices)
    content: Optional[str] = ",".join(
        [choice.message.content or "" for choice in choices]
    )
    assert content is not None
    print("======== Final Content ========")
    print(content)
    print("====== End of Final Content ======")
    assert "helix.pipelines" in content
    # assert "data:image/png;base64" in content
