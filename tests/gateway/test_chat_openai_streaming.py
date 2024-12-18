import json
from typing import List

import httpx
from httpx import Response
from openai import AsyncOpenAI, AsyncStream
from openai.types import CompletionUsage
from openai.types.chat import ChatCompletionChunk
from pytest_httpx import HTTPXMock, IteratorStream

from language_model_gateway.configs.config_schema import (
    ChatModelConfig,
    ModelConfig,
    ModelParameterConfig,
    PromptConfig,
)
from language_model_gateway.container.simple_container import SimpleContainer
from language_model_gateway.gateway.api_container import get_container_async
from language_model_gateway.gateway.utilities.environment_reader import (
    EnvironmentReader,
)
from openai.types.chat.chat_completion_chunk import ChoiceDelta, Choice as ChunkChoice

from language_model_gateway.gateway.utilities.expiring_cache import ExpiringCache


async def test_chat_completions_streaming(
    async_client: httpx.AsyncClient, httpx_mock: HTTPXMock
) -> None:
    test_container: SimpleContainer = await get_container_async()

    if not EnvironmentReader.is_environment_variable_set("RUN_TESTS_WITH_REAL_LLM"):
        chunks_json: List[ChatCompletionChunk] = [
            ChatCompletionChunk(
                id=str(0),
                created=1633660000,
                model="ChatGPT",
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
                model="ChatGPT",
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
                model="ChatGPT",
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

    model_configuration_cache: ExpiringCache[List[ChatModelConfig]] = (
        test_container.resolve(ExpiringCache)
    )
    await model_configuration_cache.set(
        [
            ChatModelConfig(
                id="b_well_phr",
                name="ChatGPT",
                description="ChatGPT",
                type="openai",
                model=ModelConfig(
                    provider="bedrock",
                    model="us.anthropic.claude-3-5-haiku-20241022-v1:0",
                ),
                url="http://host.docker.internal:5055/api/v1/chat/completions",
                model_parameters=[ModelParameterConfig(key="temperature", value=0.5)],
                system_prompts=[
                    PromptConfig(
                        role="system",
                        content='Given a task description or existing prompt, produce a detailed system prompt to guide a language model in completing the task effectively.\n\n# Guidelines\n\n- Understand the Task: Grasp the main objective, goals, requirements, constraints, and expected output.\n- Minimal Changes: If an existing prompt is provided, improve it only if it\'s simple. For complex prompts, enhance clarity and add missing elements without altering the original structure.\n- Reasoning Before Conclusions**: Encourage reasoning steps before any conclusions are reached. ATTENTION! If the user provides examples where the reasoning happens afterward, REVERSE the order! NEVER START EXAMPLES WITH CONCLUSIONS!\n    - Reasoning Order: Call out reasoning portions of the prompt and conclusion parts (specific fields by name). For each, determine the ORDER in which this is done, and whether it needs to be reversed.\n    - Conclusion, classifications, or results should ALWAYS appear last.\n- Examples: Include high-quality examples if helpful, using placeholders [in brackets] for complex elements.\n   - What kinds of examples may need to be included, how many, and whether they are complex enough to benefit from placeholders.\n- Clarity and Conciseness: Use clear, specific language. Avoid unnecessary instructions or bland statements.\n- Formatting: Use markdown features for readability. DO NOT USE ``` CODE BLOCKS UNLESS SPECIFICALLY REQUESTED.\n- Preserve User Content: If the input task or prompt includes extensive guidelines or examples, preserve them entirely, or as closely as possible. If they are vague, consider breaking down into sub-steps. Keep any details, guidelines, examples, variables, or placeholders provided by the user.\n- Constants: DO include constants in the prompt, as they are not susceptible to prompt injection. Such as guides, rubrics, and examples.\n- Output Format: Explicitly the most appropriate output format, in detail. This should include length and syntax (e.g. short sentence, paragraph, JSON, etc.)\n    - For tasks outputting well-defined or structured data (classification, JSON, etc.) bias toward outputting a JSON.\n    - JSON should never be wrapped in code blocks (```) unless explicitly requested.\n\nThe final prompt you output should adhere to the following structure below. Do not include any additional commentary, only output the completed system prompt. SPECIFICALLY, do not include any additional messages at the start or end of the prompt. (e.g. no "---")\n\n[Concise instruction describing the task - this should be the first line in the prompt, no section header]\n\n[Additional details as needed.]\n\n[Optional sections with headings or bullet points for detailed steps.]\n\n# Steps [optional]\n\n[optional: a detailed breakdown of the steps necessary to accomplish the task]\n\n# Output Format\n\n[Specifically call out how the output should be formatted, be it response length, structure e.g. JSON, markdown, etc]\n\n# Examples [optional]\n\n[Optional: 1-3 well-defined examples with placeholders if necessary. Clearly mark where examples start and end, and what the input and output are. User placeholders as necessary.]\n[If the examples are shorter than what a realistic example is expected to be, make a reference with () explaining how real examples should be longer / shorter / different. AND USE PLACEHOLDERS! ]\n\n# Notes [optional]\n\n[optional: edge cases, details, and an area to call or repeat out specific important considerations]',
                    ),
                    PromptConfig(
                        role="system",
                        content="The user will provide a Task, Goal, or Current Prompt.",
                    ),
                ],
                # tools=[
                #     ToolConfig(
                #         name="current_date"
                #     )
                # ]
            )
        ]
    )

    # init client and connect to localhost server
    client = AsyncOpenAI(
        api_key="fake-api-key",
        base_url="http://localhost:5000/api/v1",  # change the default port if needed
        http_client=async_client,
    )

    stream: AsyncStream[ChatCompletionChunk] = await client.chat.completions.create(
        model="ChatGPT",
        messages=[{"role": "user", "content": "Say this is a test"}],
        stream=True,
    )

    chunk: ChatCompletionChunk
    async for chunk in stream:
        delta_content = "\n".join(
            [choice.delta.content or "" for choice in chunk.choices]
        )
        print(delta_content)
