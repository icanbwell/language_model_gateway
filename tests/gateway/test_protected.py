import httpx


async def test_protected(async_client: httpx.AsyncClient) -> None:

    result = await async_client.get("/health")
    assert result.status_code == 200

    # call /protected endpoint
    result = await async_client.get("/protected")
    print(result)
    assert result.status_code == 401
    redirect_location = result.headers["location"]
    assert redirect_location == "/auth/login"

    # call the /auth/callback endpoint
    result = await async_client.get(redirect_location)
    print(result)
    assert result.status_code == 401
    redirect_location = result.headers["location"]
    assert redirect_location == "/auth/login"
