import logging
import time
import uuid
from typing import Dict, Any, Optional, cast
from urllib.parse import urlencode

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from language_model_gateway.gateway.utilities.tokens.well_known_configuration_reader.well_known_configuration import (
    WellKnownConfiguration,
)
from language_model_gateway.gateway.utilities.tokens.well_known_configuration_reader.well_known_configuration_reader import (
    WellKnownConfigurationReader,
)

logger = logging.getLogger(__name__)


class JwtTokenError(Exception):
    """Custom exception for JWT token-related errors"""


class JwtAuthenticator:
    def __init__(
        self,
        *,
        cookie_name: str = "jwt_token",
        cookie_max_age: int = 3600,  # 1 hour
        well_known_configuration_reader: WellKnownConfigurationReader,
        token_leeway: int = 60,  # 60 seconds token leeway
    ):
        """
        Initialize OAuth authentication using well-known configuration.

        Args:
            cookie_name (str, optional): Name of the JWT cookie
            cookie_max_age (int, optional): Cookie max age in seconds
            well_known_configuration_reader (WellKnownConfigurationReader): Configuration reader
            token_leeway (int, optional): Leeway for token expiration
        """
        self.cookie_name = cookie_name
        self.cookie_max_age = cookie_max_age
        self.well_known_configuration_reader = well_known_configuration_reader
        self.token_leeway = token_leeway

    async def get_login_url(
        self,
        *,
        client_id: str,
        redirect_uri: str,
        well_known_config_url: str,
        state: Optional[str] = None,
        scopes: Optional[str] = None,
    ) -> str:
        """
        Generate OAuth authorization URL.

        Args:
            client_id (str): OAuth client ID
            redirect_uri (str): OAuth callback redirect URI
            well_known_config_url (str): Provider's well-known configuration URL
            state (str, optional): CSRF protection state. Generated if not provided
            scopes (str, optional): OAuth scopes. Defaults to 'openid profile email'

        Returns:
            str: Authorization URL
        """
        assert self.well_known_configuration_reader

        # Generate state for CSRF protection if not provided
        state = state or str(uuid.uuid4())

        # Default scopes if not provided
        scopes = scopes or "openid profile email"

        # Construct authorization URL parameters
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": scopes,
            "state": state,
        }

        assert well_known_config_url, "Well-known configuration URL is required"

        # Fetch well-known configuration
        well_known_configuration: Optional[WellKnownConfiguration] = (
            await self.well_known_configuration_reader.fetch_configuration_async(
                well_known_config_url=well_known_config_url,
            )
        )
        assert well_known_configuration, "Failed to retrieve well-known configuration"

        # Construct full authorization URL
        auth_url = (
            f"{well_known_configuration.authorization_endpoint}?{urlencode(params)}"
        )

        logger.info(f"Generated login URL for client {client_id}")
        return auth_url

    def create_jwt_token(
        self,
        *,
        user_info: Dict[str, Any],
        jwt_secret: str,
        additional_claims: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Create a JWT token from user information.

        Args:
            user_info (Dict[str, Any]): User information from OAuth provider
            jwt_secret (str): JWT secret
            additional_claims (Dict[str, Any], optional): Additional claims to include

        Returns:
            str: Signed JWT token
        """
        # Validate jwt_secret
        if not jwt_secret:
            raise ValueError("JWT secret cannot be empty")

        # Base payload with standard claims
        current_time = int(time.time())
        payload: Dict[str, Any] = {
            "sub": user_info.get("sub", ""),
            "email": user_info.get("email", ""),
            "name": user_info.get("name", ""),
            "exp": current_time + self.cookie_max_age,
            "iat": current_time,
            "jti": str(uuid.uuid4()),  # Unique token identifier
        }

        # Add additional claims if provided
        if additional_claims:
            payload.update(additional_claims)

        try:
            token = jwt.encode(payload, jwt_secret, algorithm="HS256")
            logger.info("JWT token created successfully")
            return token
        except Exception as e:
            logger.error(f"Failed to create JWT token: {e}")
            raise JwtTokenError("Failed to create JWT token") from e

    def validate_jwt_token(
        self, *, token: str, jwt_secret: str
    ) -> Optional[Dict[str, Any]]:
        """
        Validate JWT token with enhanced error handling.

        Args:
            token (str): JWT token to validate
            jwt_secret (str): JWT secret

        Returns:
            Optional[Dict[str, Any]]: Decoded token payload or None
        """
        # Validate inputs
        if not token:
            logger.warning("Empty token provided")
            return None

        if not jwt_secret:
            logger.error("JWT secret is empty")
            return None

        try:
            # Decode with leeway for clock skew
            payload = jwt.decode(
                token,
                jwt_secret,
                algorithms=["HS256"],
                options={
                    "verify_exp": True,
                    "verify_iat": True,
                    "require_exp": True,
                    "require_iat": True,
                },
                leeway=self.token_leeway,
            )

            # Additional custom validation can be added here
            logger.info("JWT token validated successfully")
            return cast(Dict[str, Any], payload)

        except ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
        except JwtTokenError as e:
            logger.error(f"JWT decoding error: {e}")
            return None
