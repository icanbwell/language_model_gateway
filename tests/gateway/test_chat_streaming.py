import json
from typing import List

import httpx
from httpx import Response
from openai import AsyncOpenAI, AsyncStream
from openai.types import CompletionUsage
from openai.types.chat import ChatCompletionChunk
from pytest_httpx import HTTPXMock, IteratorStream

from language_model_gateway.gateway.utilities.environment_reader import (
    EnvironmentReader,
)
from openai.types.chat.chat_completion_chunk import ChoiceDelta, Choice as ChunkChoice


async def test_chat_completions_streaming(
    async_client: httpx.AsyncClient, httpx_mock: HTTPXMock
) -> None:
    if not EnvironmentReader.is_environment_variable_set("RUN_TESTS_WITH_REAL_LLM"):
        chunks_json: List[ChatCompletionChunk] = [
            ChatCompletionChunk(
                id=str(0),
                created=1633660000,
                model="b.well PHR",
                choices=[
                    ChunkChoice(
                        index=0,
                        delta=ChoiceDelta(role="assistant", content="This" + " "),
                    )
                ],
                usage=CompletionUsage(
                    prompt_tokens=0, completion_tokens=0, total_tokens=0
                ),
                object="chat.completion.chunk",
            ),
            ChatCompletionChunk(
                id=str(0),
                created=1633660000,
                model="b.well PHR",
                choices=[
                    ChunkChoice(
                        index=0,
                        delta=ChoiceDelta(role="assistant", content="is a" + " "),
                    )
                ],
                usage=CompletionUsage(
                    prompt_tokens=0, completion_tokens=0, total_tokens=0
                ),
                object="chat.completion.chunk",
            ),
            ChatCompletionChunk(
                id=str(0),
                created=1633660000,
                model="b.well PHR",
                choices=[
                    ChunkChoice(
                        index=0,
                        delta=ChoiceDelta(role="assistant", content="test" + " "),
                    )
                ],
                usage=CompletionUsage(
                    prompt_tokens=0, completion_tokens=0, total_tokens=0
                ),
                object="chat.completion.chunk",
            ),
        ]
        chunks: List[bytes] = [
            f"data: {json.dumps(chunks_json[0].model_dump())}\n\n".encode("utf-8"),
            f"data: {json.dumps(chunks_json[1].model_dump())}\n\n".encode("utf-8"),
            f"data: {json.dumps(chunks_json[2].model_dump())}\n\n".encode("utf-8"),
            b"data: [DONE]\n\n",
        ]
        httpx_mock.add_callback(
            callback=lambda request: Response(
                status_code=200,
                headers={"Content-Type": "text/event-stream"},
                stream=IteratorStream(chunks),
            ),
            url="http://host.docker.internal:5055/api/v1/chat/completions",
        )

    # init client and connect to localhost server
    client = AsyncOpenAI(
        api_key="fake-api-key",
        base_url="http://localhost:5000/api/v1",  # change the default port if needed
        http_client=async_client,
    )

    stream: AsyncStream[ChatCompletionChunk] = await client.chat.completions.create(
        model="b.well PHR",
        messages=[{"role": "user", "content": "Say this is a test"}],
        stream=True,
    )
    async for chunk in stream:
        delta_content = "\n".join(
            [choice.delta.content or "" for choice in chunk.choices]
        )
        print(delta_content)
