import httpx
import pytest
from openai import AsyncOpenAI
from openai.types import ImagesResponse


@pytest.mark.asyncio
async def test_chat_anthropic_image_generation(async_client: httpx.AsyncClient) -> None:
    print("")

    # if not EnvironmentReader.is_environment_variable_set("RUN_TESTS_WITH_REAL_LLM"):
    #     test_container: SimpleContainer = await get_container_async()
    #     test_container.register(
    #         ModelFactory,
    #         lambda c: MockModelFactory(
    #             fn_get_model=lambda chat_model_config: MockChatModel(
    #                 fn_get_response=lambda messages: "His first name is Barack"
    #             )
    #         ),
    #     )
    #     test_container.register(
    #         ImageGeneratorFactory,
    #         lambda c: MockImageGeneratorFactory(image_generator=MockImageGenerator()),
    #     )

    # init client and connect to localhost server
    client = AsyncOpenAI(
        api_key="fake-api-key",
        base_url="http://localhost:5000/api/v1",  # change the default port if needed
        http_client=async_client,
    )

    # call API
    response: ImagesResponse = await client.images.generate(
        model="dall-e-3",
        prompt="a white siamese cat",
        size="1024x1024",
        quality="standard",
        n=1,
    )

    assert response.data is not None
    image_url = response.data[0].url
    print(f"Image URL: {image_url}")
    assert image_url is not None
    assert "http" in image_url
