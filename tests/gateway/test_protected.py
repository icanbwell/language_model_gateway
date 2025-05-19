import re
from typing import override, Optional

import httpx
from pytest_httpx import HTTPXMock

from language_model_gateway.container.simple_container import SimpleContainer
from language_model_gateway.gateway.api_container import get_container_async
from language_model_gateway.gateway.http.http_client_factory import HttpClientFactory
from language_model_gateway.gateway.utilities.tokens.well_known_configuration_reader.well_known_configuration import (
    WellKnownConfiguration,
)
from language_model_gateway.gateway.utilities.tokens.well_known_configuration_reader.well_known_configuration_reader import (
    WellKnownConfigurationReader,
)


class MockWellKnownConfigurationReader(WellKnownConfigurationReader):
    @override
    async def fetch_configuration_async(
        self, *, well_known_config_url: str
    ) -> Optional[WellKnownConfiguration]:
        return WellKnownConfiguration(
            authorization_endpoint="https://example.com/auth",
            token_endpoint="https://example.com/token",
            userinfo_endpoint="https://example.com/userinfo",
            jwks_uri="https://example.com/jwks",
            issuer="https://example.com",
            end_session_endpoint="https://example.com/logout",
            scopes_supported=["openid", "profile", "email"],
            response_types_supported=["code", "token"],
            token_endpoint_auth_methods_supported=["client_secret_basic"],
            revocation_endpoint="https://example.com/revoke",
            introspection_endpoint="https://example.com/introspect",
        )


async def test_protected(
    async_client: httpx.AsyncClient, httpx_mock: HTTPXMock
) -> None:
    # Mock the specific URL
    # Prepare the full OAuth URL
    # base_url = "https://example.com/auth"
    # client_id = (
    #     "35389918383-nq3htpm1keas26nce75kfp04nl7vtf64.apps.googleusercontent.com"
    # )
    # redirect_uri = "http%3A%2F%2Flocalhost%3A5050%2Foauth2%2Fcallback"

    base_url_pattern = re.compile(r".*example.*")

    test_container: SimpleContainer = await get_container_async()
    test_container.register(
        WellKnownConfigurationReader,
        lambda c: MockWellKnownConfigurationReader(
            http_client_factory=c.resolve(HttpClientFactory),
        ),
    )

    result = await async_client.get("/health")
    assert result.status_code == 200

    # Call /protected endpoint
    result = await async_client.get("/protected")
    assert result.status_code == 401
    redirect_location = result.headers["location"]
    assert redirect_location == "/auth/login"

    # Call the /auth/callback endpoint
    result = await async_client.get(redirect_location)
    assert result.status_code == 302
    redirect_location = result.headers["location"]
    print(f"redirect_location: {redirect_location}")

    # Add mock response with the precise URL matching
    httpx_mock.add_response(
        # allow any url that starts with the base_url
        url=base_url_pattern,
        method="GET",
        json={
            "code": "123",
        },
        status_code=200,
    )

    async with HttpClientFactory().create_http_client(
        base_url=redirect_location
    ) as client:
        response = await client.get(redirect_location)
        assert response.status_code == 200
        assert result.json() == {"message": "Mocked auth response"}
