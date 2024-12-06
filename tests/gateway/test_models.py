import httpx
from openai import AsyncOpenAI
from openai.pagination import AsyncPage
from openai.types import Model


async def test_models(async_client: httpx.AsyncClient) -> None:
    # init client and connect to localhost server
    # init client and connect to localhost server
    client = AsyncOpenAI(
        api_key="fake-api-key",
        base_url="http://localhost:5000/api/v1",  # change the default port if needed
        http_client=async_client,
    )
    models: AsyncPage[Model] = await client.models.list()
    print(models.model_dump_json())
    assert models
    mode: Model
    i = 0
    async for model in models:
        i += 1
        print(model.id)
        assert model.id

    assert i > 0, f"Expected at least one model, but got {i}"
