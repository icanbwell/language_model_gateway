import os

import httpx
import pytest
from httpx import Response
from pytest_httpx import HTTPXMock

from language_model_gateway.container.simple_container import SimpleContainer
from language_model_gateway.gateway.api_container import get_container_async
from language_model_gateway.gateway.models.model_factory import ModelFactory
from language_model_gateway.gateway.utilities.environment_reader import (
    EnvironmentReader,
)
from language_model_gateway.gateway.utilities.tokens.jwt_authenticator.jwt_authenticator import (
    JwtAuthenticator,
)
from tests.gateway.mocks.mock_chat_model import MockChatModel
from tests.gateway.mocks.mock_model_factory import MockModelFactory


@pytest.mark.asyncio
async def test_login(async_client: httpx.AsyncClient, httpx_mock: HTTPXMock) -> None:
    print("")

    if not EnvironmentReader.is_environment_variable_set("RUN_TESTS_WITH_REAL_LLM"):
        test_container: SimpleContainer = await get_container_async()
        test_container.register(
            ModelFactory,
            lambda c: MockModelFactory(
                fn_get_model=lambda chat_model_config: MockChatModel(
                    fn_get_response=lambda messages: "Barack"
                )
            ),
        )
        jwt_authenticator: JwtAuthenticator = test_container.resolve(JwtAuthenticator)
        client_id = os.getenv("CLIENT_ID", "")
        well_known_config_url = os.getenv("OAUTH_WELL_KNOWN_URL", "")
        prefix: str = "/auth"
        redirect_uri = os.getenv(
            "OAUTH_REDIRECT_URI", f"http://localhost:8000{prefix}/callback"
        )
        httpx_mock.add_callback(
            callback=lambda request: Response(
                200,
                json={
                    "authorization_endpoint": "123",
                    "token_endpoint": "",
                    "userinfo_endpoint": "",
                },
            ),
            url=well_known_config_url,
        )

        auth_url = await jwt_authenticator.get_login_url(
            client_id=client_id,
            redirect_uri=redirect_uri,
            well_known_config_url=well_known_config_url,
        )
        # Test health endpoint
        response = await async_client.get(auth_url)
        assert response.status_code == 200

    # Test health endpoint
    response = await async_client.get("/health")
    assert response.status_code == 200
