from typing import override, Optional

import httpx

from language_model_gateway.container.simple_container import SimpleContainer
from language_model_gateway.gateway.api_container import get_container_async
from language_model_gateway.gateway.utilities.tokens.well_known_configuration_reader.well_known_configuration import (
    WellKnownConfiguration,
)
from language_model_gateway.gateway.utilities.tokens.well_known_configuration_reader.well_known_configuration_reader import (
    WellKnownConfigurationReader,
)


class MockWellKnownConfigurationReader(WellKnownConfigurationReader):
    @override
    def read_from_well_known_configuration(
        self, *, well_known_config_url: str
    ) -> Optional[WellKnownConfiguration]:
        return WellKnownConfiguration(
            authorization_endpoint="https://example.com/auth",
            token_endpoint="https://example.com/token",
            userinfo_endpoint="https://example.com/userinfo",
        )


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
    test_container: SimpleContainer = await get_container_async()
    test_container.register(
        WellKnownConfigurationReader, lambda c: MockWellKnownConfigurationReader()
    )

    result = await async_client.get(redirect_location)
    print(result)
    assert result.status_code == 401
    redirect_location = result.headers["location"]
    assert redirect_location == "/auth/login"
