import logging
import time
import uuid
import jwt
from typing import Dict, Any, Optional, cast
from urllib.parse import urlencode

from language_model_gateway.gateway.utilities.tokens.well_known_configuration_reader.well_known_configuration import (
    WellKnownConfiguration,
)
from language_model_gateway.gateway.utilities.tokens.well_known_configuration_reader.well_known_configuration_reader import (
    WellKnownConfigurationReader,
)

logger = logging.getLogger(__name__)


class JwtAuthenticator:
    def __init__(
        self,
        *,
        cookie_name: str = "jwt_token",
        cookie_max_age: int = 3600,  # 1 hour
        well_known_configuration_reader: WellKnownConfigurationReader,
    ):
        """
        Initialize OAuth authentication using well-known configuration.

        Args:
            cookie_name (str, optional): Name of the JWT cookie
            cookie_max_age (int, optional): Cookie max age in seconds
        """
        self.cookie_name = cookie_name
        self.cookie_max_age = cookie_max_age
        self.well_known_configuration_reader = well_known_configuration_reader

    async def get_login_url(
        self,
        *,
        client_id: str,
        redirect_uri: str,
        well_known_config_url: str,
    ) -> str:
        """
        Generate OAuth authorization URL.

        :param client_id: OAuth client ID
        :param redirect_uri: OAuth callback redirect URI
        :param well_known_config_url: Provider's well-known configuration URL
        :return: Authorization URL
        """
        assert self.well_known_configuration_reader
        # Generate state for CSRF protection
        state = str(uuid.uuid4())
        # Construct authorization URL
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid profile email",
            "state": state,
        }
        assert well_known_config_url
        well_known_configuration: WellKnownConfiguration | None = (
            await self.well_known_configuration_reader.read_from_well_known_configuration_async(
                well_known_config_url=well_known_config_url,
            )
        )
        assert well_known_configuration
        auth_url = (
            f"{well_known_configuration.authorization_endpoint}?{urlencode(params)}"
        )
        return auth_url

    def create_jwt_token(self, *, user_info: Dict[str, Any], jwt_secret: str) -> str:
        """
        Create a JWT token from user information.

        Args:
            user_info (Dict[str, Any]): User information from OAuth provider
            jwt_secret (str): JWT secret

        Returns:
            str: Signed JWT token
        """
        payload = {
            "sub": user_info.get("sub", ""),
            "email": user_info.get("email", ""),
            "name": user_info.get("name", ""),
            "exp": int(time.time()) + self.cookie_max_age,
            "iat": int(time.time()),
        }

        return jwt.encode(payload, jwt_secret or "", algorithm="HS256")

    # noinspection PyMethodMayBeStatic
    def validate_jwt_token(
        self, *, token: str, jwt_secret: str
    ) -> Optional[Dict[str, Any]]:
        """
        Validate JWT token.

        Args:
            token (str): JWT token to validate
            jwt_secret (str): JWT secret

        Returns:
            Optional[Dict[str, Any]]: Decoded token payload or None
        """
        assert jwt_secret
        try:
            payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
            return cast(Dict[str, Any], payload)
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None
