import logging
from typing import Optional, Dict, Any, cast

import requests

from language_model_gateway.gateway.utilities.tokens.well_known_configuration_reader.well_known_configuration import (
    WellKnownConfiguration,
)

logger = logging.getLogger(__name__)


class WellKnownConfigurationReader:
    def read_from_well_known_configuration(
        self, *, well_known_config_url: str
    ) -> Optional[WellKnownConfiguration]:
        config: Dict[str, Any] = self._fetch_well_known_configuration(
            well_known_config_url=well_known_config_url
        )

        return WellKnownConfiguration(
            authorization_endpoint=config.get("authorization_endpoint"),
            token_endpoint=config.get("token_endpoint"),
            userinfo_endpoint=config.get("userinfo_endpoint"),
        )

    @staticmethod
    def _fetch_well_known_configuration(
        *, well_known_config_url: str
    ) -> Dict[str, Any]:
        """
        Fetch OpenID provider configuration.

        Returns:
            Dict[str, Any]: OpenID configuration

        Raises:
            ValueError: If configuration cannot be retrieved
        """
        assert well_known_config_url, "Well-known configuration URL is required"
        try:
            response = requests.get(well_known_config_url)
            response.raise_for_status()
            return cast(Dict[str, Any], response.json())
        except requests.RequestException as e:
            logger.error(f"Failed to fetch well-known configuration: {e}")
            raise ValueError(f"Failed to fetch well-known configuration: {e}")
