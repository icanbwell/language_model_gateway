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


import re
import httpx
import urllib.parse
from typing import Dict, Any, Optional


async def test_protected(
        async_client: httpx.AsyncClient,
        httpx_mock: HTTPXMock
) -> None:
    # OAuth Configuration
    base_url = "https://example.com/auth"
    client_id = "35389918383-nq3htpm1keas26nce75kfp04nl7vtf64.apps.googleusercontent.com"
    redirect_uri = "http%3A%2F%2Flocalhost%3A5050%2Foauth2%2Fcallback"

    # Utility function to create regex patterns for URL matching
    def create_url_regex(
            base_url: str,
            path: Optional[str] = None,
            query_params: Optional[Dict[str, str]] = None
    ) -> re.Pattern:
        """
        Create a comprehensive regex pattern for URL matching

        Args:
            base_url (str): Base URL to match
            path (str, optional): Specific path to match
            query_params (Dict[str, str], optional): Expected query parameters

        Returns:
            re.Pattern: Compiled regex pattern for URL matching
        """
        # Escape special characters in base URL
        escaped_base_url = re.escape(base_url)

        # Construct base regex pattern
        pattern = f"^{escaped_base_url}"

        # Add path matching if provided
        if path:
            pattern += re.escape(path)

        # Add query parameter matching
        if query_params:
            query_parts = []
            for key, value in query_params.items():
                # URL encode the value to match real-world scenarios
                encoded_value = urllib.parse.quote(value)
                query_parts.append(f"{re.escape(key)}={re.escape(encoded_value)}")

            pattern += r"\?" + r"&".join(query_parts)

        # Allow additional query parameters
        pattern += r".*$"

        return re.compile(pattern)

    # Regex Patterns for Different Endpoints
    # 1. Authorization Endpoint Regex
    authorization_regex = create_url_regex(
        base_url,
        path="/authorize",
        query_params={
            "client_id": client_id,
            "redirect_uri": urllib.parse.unquote(redirect_uri),
            "response_type": "code"
        }
    )

    # 2. Token Endpoint Regex
    token_regex = re.compile(
        r"^https://example\.com/auth/token.*$"
    )

    # 3. User Info Endpoint Regex
    userinfo_regex = re.compile(
        r"^https://example\.com/auth/userinfo.*$"
    )

    # 4. Well-Known Configuration Endpoint Regex
    well_known_regex = re.compile(
        r"^https://example\.com/auth/\.well-known/openid-configuration.*$"
    )

    # Mock Endpoints Setup
    # 1. Authorization Endpoint Mock
    httpx_mock.add_response(
        url=authorization_regex,
        method="GET",
        status_code=302,
        headers={
            "location": (
                f"http://localhost:5050/oauth2/callback?"
                f"code=SplxlOBeZQQYbYS6WxSbIA&"
                f"state=xyz"
            )
        }
    )

    # 2. Token Endpoint Mock
    httpx_mock.add_response(
        url=token_regex,
        method="POST",
        json={
            "access_token": "mock_access_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "mock_refresh_token",
            "id_token": "mock_id_token"
        },
        status_code=200
    )

    # 3. User Info Endpoint Mock
    httpx_mock.add_response(
        url=userinfo_regex,
        method="GET",
        json={
            "sub": "1234567890",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "picture": "https://example.com/profile.jpg"
        },
        status_code=200
    )

    # 4. Well-Known Configuration Endpoint Mock
    httpx_mock.add_response(
        url=well_known_regex,
        method="GET",
        json={
            "issuer": "https://example.com/auth",
            "authorization_endpoint": f"{base_url}/authorize",
            "token_endpoint": f"{base_url}/token",
            "userinfo_endpoint": f"{base_url}/userinfo",
            "jwks_uri": f"{base_url}/jwks"
        },
        status_code=200
    )

    # Debugging Utility Function
    def debug_url_matching(url: str, patterns: Dict[str, re.Pattern]) -> Dict[str, bool]:
        """
        Debug URL matching against multiple regex patterns

        Args:
            url (str): URL to test
            patterns (Dict[str, re.Pattern]): Patterns to match against

        Returns:
            Dict[str, bool]: Matching results for each pattern
        """
        return {
            name: pattern.match(url) is not None
            for name, pattern in patterns.items()
        }

    # Comprehensive Pattern Collection for Debugging
    debug_patterns = {
        "Authorization": authorization_regex,
        "Token": token_regex,
        "UserInfo": userinfo_regex,
        "WellKnown": well_known_regex
    }

    # # Setup container and mock configurations
    # test_container: SimpleContainer = await get_container_async()
    # test_container.register(
    #     WellKnownConfigurationReader,
    #     lambda c: MockWellKnownConfigurationReader(
    #         http_client_factory=c.resolve(HttpClientFactory),
    #     ),
    # )

    # Health check
    result = await async_client.get("/health")
    assert result.status_code == 200

    # Test protected endpoint
    result = await async_client.get("/protected")
    assert result.status_code == 401

    # Verify redirect to login
    redirect_location = result.headers["location"]
    assert redirect_location == "/auth/login"

    # Simulate login redirect
    result = await async_client.get(redirect_location)
    assert result.status_code == 302

    # Get the redirect location (simulated OAuth authorization)
    redirect_location = result.headers["location"]
    print(f"OAuth Redirect Location: {redirect_location}")

    # Optional: Debug URL matching
    matching_results = debug_url_matching(redirect_location, debug_patterns)
    print("URL Matching Debug:", matching_results)

    # Verify the OAuth callback
    async with HttpClientFactory().create_http_client(
            base_url=redirect_location
    ) as client:
        response = await client.get(redirect_location)

        # Assert successful authentication
        assert response.status_code == 200
        assert response.json() == {
            "message": "Authentication successful",
            "user": {
                "id": "1234567890",
                "name": "John Doe",
                "email": "john.doe@example.com"
            }
        }
