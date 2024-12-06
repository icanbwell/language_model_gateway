import httpx
import pytest
from openai import AsyncOpenAI, AsyncStream
from openai.types.chat import ChatCompletionChunk

from language_model_gateway.container.simple_container import SimpleContainer
from language_model_gateway.gateway.api_container import get_container_async
from language_model_gateway.gateway.models.model_factory import ModelFactory
from language_model_gateway.gateway.utilities.environment_reader import (
    EnvironmentReader,
)
from tests.gateway.mocks.mock_chat_model import MockChatModel
from tests.gateway.mocks.mock_model_factory import MockModelFactory


@pytest.mark.asyncio
async def test_chat_completions_streaming(async_client: httpx.AsyncClient) -> None:
    print("")

    if not EnvironmentReader.is_environment_variable_set("RUN_TESTS_WITH_REAL_LLM"):
        test_container: SimpleContainer = await get_container_async()

        test_container.register(
            ModelFactory,
            lambda c: MockModelFactory(
                fn_get_model=lambda chat_model_config: MockChatModel(
                    fn_get_response=lambda messages: "His first name is Barack"
                )
            ),
        )

    # init client and connect to localhost server
    client = AsyncOpenAI(
        api_key="fake-api-key",
        base_url="http://localhost:5000/api/v1",  # change the default port if needed
        http_client=async_client,
    )

    # call API
    stream: AsyncStream[ChatCompletionChunk] = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "what is the first name of Obama?",
            }
        ],
        model="General Purpose",
        stream=True,
    )
    content: str = ""
    i: int = 0
    async for chunk in stream:
        i += 1
        print(f"======== Chunk {i} ========")
        delta_content = "\n".join(
            [choice.delta.content or "" for choice in chunk.choices]
        )
        content += delta_content or ""
        print(delta_content or "")
        print(f"====== End of Chunk {i} ======")

    print("======== Final Content ========")
    print(content)
    print("====== End of Final Content ======")
    assert "Barack" in content


@pytest.mark.asyncio
async def test_chat_completions_with_chat_history_streaming(
    async_client: httpx.AsyncClient,
) -> None:
    print("")

    if not EnvironmentReader.is_environment_variable_set("RUN_TESTS_WITH_REAL_LLM"):
        test_container: SimpleContainer = await get_container_async()

        test_container.register(
            ModelFactory,
            lambda c: MockModelFactory(
                fn_get_model=lambda chat_model_config: MockChatModel(
                    fn_get_response=lambda messages: "His first name is Barack"
                )
            ),
        )

    # init client and connect to localhost server
    client = AsyncOpenAI(
        api_key="fake-api-key",
        base_url="http://localhost:5000/api/v1",  # change the default port if needed
        http_client=async_client,
    )

    # call API
    stream: AsyncStream[ChatCompletionChunk] = await client.chat.completions.create(
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
        model="General Purpose",
        stream=True,
    )
    content: str = ""
    i: int = 0
    async for chunk in stream:
        i += 1
        print(f"======== Chunk {i} ========")
        delta_content = "\n".join(
            [choice.delta.content or "" for choice in chunk.choices]
        )
        content += delta_content or ""
        print(delta_content or "")
        print(f"====== End of Chunk {i} ======")

    print("======== Final Content ========")
    print(content)
    print("====== End of Final Content ======")
    assert "Barack" in content
