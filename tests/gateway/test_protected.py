import httpx


async def test_protected(async_client: httpx.AsyncClient) -> None:

    response = await async_client.get("/health")
    assert response.status_code == 200

    # call /protected endpoint
    result = await async_client.get("/protected")
    print(result)
    assert result.status_code == 401
    assert result.headers["location"] == "http://localhost:8000/auth/callback"
