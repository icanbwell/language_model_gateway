from typing import Optional, List

import httpx
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from language_model_gateway.configs.config_schema import (
    ChatModelConfig,
    ModelConfig,
    AgentConfig,
    PromptConfig,
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


async def test_chat_anthropic_with_pdf_scraping(
    async_client: httpx.AsyncClient,
) -> None:
    test_container: SimpleContainer = await get_container_async()
    if not EnvironmentReader.is_environment_variable_set("RUN_TESTS_WITH_REAL_LLM"):
        test_container.register(
            ModelFactory,
            lambda c: MockModelFactory(
                fn_get_model=lambda chat_model_config: MockChatModel(
                    fn_get_response=lambda messages: "USPSTF"
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
                id="parse_web_page",
                name="Parse Web Page",
                description="Parse Web Page",
                type="langchain",
                model=ModelConfig(
                    provider="bedrock",
                    model="us.anthropic.claude-3-5-haiku-20241022-v1:0",
                ),
                system_prompts=[
                    PromptConfig(
                        role="system",
                        content="You are an assistant that parses web pages.  Let’s think step by step and take your time to get the right answer.  Try the get_web_page tool first and if you don't get the answer then use the scraping_bee_web_scraper tool.",
                    )
                ],
                tools=[
                    AgentConfig(name="google_search"),
                    AgentConfig(name="get_web_page"),
                    AgentConfig(name="pdf_text_extractor"),
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
                "content": "Get the definition of Prevention TaskForce from https://www.uspreventiveservicestaskforce.org/files/preventiontaskforce_data_api_wi_wlink.pdf",
            }
        ],
        model="Parse Web Page",
    )

    print(chat_completion)
    # print the top "choice"
    content: Optional[str] = "\n".join(
        choice.message.content or "" for choice in chat_completion.choices
    )
    assert content is not None
    print(content)
    assert "USPSTF" in content


async def test_chat_anthropic_with_pdf_ocr_scraping(
    async_client: httpx.AsyncClient,
) -> None:
    test_container: SimpleContainer = await get_container_async()
    if not EnvironmentReader.is_environment_variable_set("RUN_TESTS_WITH_REAL_LLM"):
        test_container.register(
            ModelFactory,
            lambda c: MockModelFactory(
                fn_get_model=lambda chat_model_config: MockChatModel(
                    fn_get_response=lambda messages: "23%"
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
                id="parse_web_page",
                name="Parse Web Page",
                description="Parse Web Page",
                type="langchain",
                model=ModelConfig(
                    provider="bedrock",
                    model="us.anthropic.claude-3-5-haiku-20241022-v1:0",
                ),
                system_prompts=[
                    PromptConfig(
                        role="system",
                        content="You are an assistant that parses web pages.  Let’s think step by step and take your time to get the right answer.  Try the get_web_page tool first and if you don't get the answer then use the scraping_bee_web_scraper tool.",
                    )
                ],
                tools=[
                    AgentConfig(name="google_search"),
                    AgentConfig(name="get_web_page"),
                    AgentConfig(name="pdf_text_extractor"),
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
                "content": "Get the debt to capitalization rate from https://emma.msrb.org/P21807566.pdf",
            }
        ],
        model="Parse Web Page",
    )

    print(chat_completion)
    # print the top "choice"
    content: Optional[str] = "\n".join(
        choice.message.content or "" for choice in chat_completion.choices
    )
    assert content is not None
    print(content)
    assert "23%" in content
