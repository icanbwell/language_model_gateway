from typing import Optional

import httpx
from httpx import Response
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion
from pytest_httpx import HTTPXMock

from language_model_gateway.gateway.utilities.environment_reader import (
    EnvironmentReader,
)


async def test_chat_completions_b_well(
    async_client: httpx.AsyncClient, httpx_mock: HTTPXMock
) -> None:

    if not EnvironmentReader.is_environment_variable_set("RUN_TESTS_WITH_REAL_LLM"):
        httpx_mock.add_callback(
            callback=lambda request: Response(
                200,
                json={
                    "id": "chat_1",
                    "object": "chat.completion",
                    "created": 1633660000,
                    "model": "b.well PHR",
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "index": 0,
                            "message": {
                                "content": "This is a test",
                                "role": "assistant",
                            },
                        }
                    ],
                },
            ),
            url="http://host.docker.internal:5055/api/v1/chat/completions",
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
                "content": "Say this is a test",
            }
        ],
        model="b.well PHR",
    )

    # print the top "choice"
    content: Optional[str] = "\n".join(
        choice.message.content or "" for choice in chat_completion.choices
    )
    print(content)
