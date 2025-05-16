from typing import Dict, Any, Optional

import httpx
from cachetools import LRUCache

from language_model_gateway.gateway.http.http_client_factory import HttpClientFactory
from language_model_gateway.gateway.utilities.tokens.well_known_configuration_reader.well_known_configuration import (
    WellKnownConfiguration,
)


class WellKnownConfigurationReader:
    """
    Well-known configuration manager
    """

    # Static cache for configuration data
    _cache: LRUCache[str, WellKnownConfiguration] = LRUCache(maxsize=100)

    def __init__(
        self,
        *,
        http_client_factory: HttpClientFactory,
    ):
        """
        Constructor
        """
        self.http_client_factory: HttpClientFactory = http_client_factory

    @staticmethod
    async def _extract_configuration_details(
        config: Dict[str, Any],
    ) -> WellKnownConfiguration:
        """
        Extract specific fields from configuration data
        :param config: Raw configuration object
        :return: Extracted configuration details
        """
        if not config or not isinstance(config, dict):
            raise ValueError("Invalid configuration data")

        return WellKnownConfiguration(
            authorization_endpoint=config.get("authorization_endpoint"),
            token_endpoint=config.get("token_endpoint"),
            userinfo_endpoint=config.get("userinfo_endpoint"),
            jwks_uri=config.get("jwks_uri"),
            issuer=config.get("issuer"),
            end_session_endpoint=config.get("end_session_endpoint"),
            scopes_supported=config.get("scopes_supported", []),
            response_types_supported=config.get("response_types_supported", []),
            token_endpoint_auth_methods_supported=config.get(
                "token_endpoint_auth_methods_supported", []
            ),
            revocation_endpoint=config.get("revocation_endpoint"),
            introspection_endpoint=config.get("introspection_endpoint"),
        )

    async def fetch_configuration_async(
        self, *, well_known_config_url: str
    ) -> Optional[WellKnownConfiguration]:
        """
        Fetch configuration data from a given URL
        :param well_known_config_url: Configuration endpoint URL
        :return: Fetched configuration data
        """
        # Check cache first
        if well_known_config_url in self._cache:
            return self._cache[well_known_config_url]

        async with self.http_client_factory.create_http_client(
            base_url=well_known_config_url
        ) as client:
            try:
                response = await client.get(well_known_config_url)
                response.raise_for_status()
                extracted_data = await self._extract_configuration_details(
                    response.json()
                )

                # Cache the extracted data
                self._cache[well_known_config_url] = extracted_data

                return extracted_data
            except httpx.RequestError as exc:
                raise RuntimeError(
                    f"Failed to fetch configuration from {well_known_config_url}: {exc}"
                ) from exc
            except httpx.HTTPStatusError as exc:
                raise RuntimeError(
                    f"Failed to fetch configuration from {well_known_config_url}: {exc.response.text}"
                ) from exc
