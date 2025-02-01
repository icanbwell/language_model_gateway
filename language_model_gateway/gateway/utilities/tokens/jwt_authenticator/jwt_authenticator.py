import time
from typing import Dict, Optional, Any, cast
from urllib.parse import urlencode

import jwt
import requests


class WellKnownOAuthAuthenticator:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        well_known_config_url: str,
        jwt_secret: str,
        redirect_uri: str,
        cookie_name: str = "jwt_token",
        cookie_max_age: int = 3600,  # 1 hour
    ):
        """
        Initialize OAuth authentication using well-known configuration.

        Args:
            client_id (str): OAuth client ID
            client_secret (str): OAuth client secret
            well_known_config_url (str): Provider's well-known configuration URL
            jwt_secret (str): Secret for JWT token signing
            redirect_uri (str): OAuth callback redirect URI
            cookie_name (str, optional): Name of the JWT cookie
            cookie_max_age (int, optional): Cookie max age in seconds
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.jwt_secret = jwt_secret
        self.cookie_name = cookie_name
        self.cookie_max_age = cookie_max_age

        # Fetch and store OpenID configuration
        self.config = self._fetch_well_known_configuration(well_known_config_url)

        # Extract important endpoints
        self.authorization_endpoint = self.config.get("authorization_endpoint")
        self.token_endpoint = self.config.get("token_endpoint")
        self.userinfo_endpoint = self.config.get("userinfo_endpoint")
        self.jwks_uri = self.config.get("jwks_uri")

        # Validate required endpoints
        self._validate_endpoints()

    def _fetch_well_known_configuration(
        self, well_known_config_url: str
    ) -> Dict[str, Any]:
        """
        Fetch OpenID provider configuration.

        Args:
            well_known_config_url (str): URL of well-known configuration

        Returns:
            Dict[str, Any]: OpenID configuration

        Raises:
            ValueError: If configuration cannot be retrieved
        """
        try:
            response = requests.get(well_known_config_url)
            response.raise_for_status()
            return cast(Dict[str, Any], response.json())
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch well-known configuration: {e}")

    def _validate_endpoints(self) -> None:
        """
        Validate that required endpoints are present.

        Raises:
            ValueError: If any required endpoint is missing
        """
        required_endpoints = [
            "authorization_endpoint",
            "token_endpoint",
            "userinfo_endpoint",
        ]

        for endpoint in required_endpoints:
            if not getattr(self, endpoint):
                raise ValueError(f"Missing {endpoint} in well-known configuration")

    def create_jwt_token(self, user_info: Dict[str, Any]) -> str:
        """
        Create a JWT token from user information.

        Args:
            user_info (Dict[str, Any]): User information from OAuth provider

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

        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")

    def validate_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate JWT token.

        Args:
            token (str): JWT token to validate

        Returns:
            Optional[Dict[str, Any]]: Decoded token payload or None
        """
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            return cast(Dict[str, Any], payload)
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def get_oauth_authorization_url(self, state: str) -> str:
        """
        Generate OAuth authorization URL.

        Args:
            state (str): CSRF protection state

        Returns:
            str: Authorization URL
        """
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "openid profile email",
            "state": state,
        }

        return f"{self.authorization_endpoint}?{urlencode(params)}"

    def exchange_code_for_token(self, authorization_code: str) -> Dict[str, str]:
        """
        Exchange authorization code for access token.

        Args:
            authorization_code (str): Authorization code from OAuth provider

        Returns:
            Dict[str, str]: Token response
        """
        assert self.token_endpoint
        token_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": authorization_code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }

        response = requests.post(self.token_endpoint, data=token_data)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())

    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """
        Retrieve user information using access token.

        Args:
            access_token (str): Access token from OAuth provider

        Returns:
            Dict[str, Any]: User information
        """
        assert self.userinfo_endpoint
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(self.userinfo_endpoint, headers=headers)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())
