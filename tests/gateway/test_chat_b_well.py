import httpx
import pytest
from openai import OpenAI
from openai.types.chat import ChatCompletion

from language_model_gateway.container.simple_container import SimpleContainer
from language_model_gateway.gateway.api_container import get_container_async
from language_model_gateway.gateway.models.model_factory import ModelFactory
from language_model_gateway.gateway.utilities.environment_reader import (
    EnvironmentReader,
)
from tests.gateway.mocks.mock_chat_model import MockChatModel
from tests.gateway.mocks.mock_model_factory import MockModelFactory


@pytest.mark.asyncio
async def test_chat_completions_b_well(
    async_client: httpx.AsyncClient, sync_client: httpx.Client
) -> None:

    if not EnvironmentReader.is_environment_variable_set("RUN_TESTS_WITH_REAL_LLM"):
        test_container: SimpleContainer = await get_container_async()
        test_container.register(
            ModelFactory,
            lambda c: MockModelFactory(
                fn_get_model=lambda model_config: MockChatModel(
                    fn_get_response=lambda messages: "This is a test"
                )
            ),
        )

    # Test health endpoint
    response = await async_client.get("/health")
    assert response.status_code == 200

    # init client and connect to localhost server
    client = OpenAI(
        api_key="fake-api-key",
        base_url="http://localhost:5000/api/v1",  # change the default port if needed
        http_client=sync_client,
    )

    # call API
    chat_completion: ChatCompletion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="b.well PHR",
    )

    # print the top "choice"
    print(chat_completion.choices[0].message.content)
