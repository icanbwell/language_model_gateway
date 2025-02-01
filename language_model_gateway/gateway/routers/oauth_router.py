import logging
import os
import time
import uuid
from enum import Enum
from typing import Optional, Dict, Any, List, cast, Sequence
from urllib.parse import urlencode

import jwt
import requests
from fastapi import APIRouter, Request, HTTPException
from fastapi.params import Depends
from fastapi.responses import RedirectResponse

from language_model_gateway.gateway.utilities.tokens.well_known_configuration_reader.well_known_configuration_reader import (
    WellKnownConfigurationReader,
)

logger = logging.getLogger(__name__)


class OAuthRouter:
    """
    Router class for OAuth authentication and token management
    """

    def __init__(
        self,
        *,
        prefix: str = "/auth",
        tags: List[str | Enum] | None = None,
        dependencies: Sequence[Depends] | None = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        well_known_config_url: Optional[str] = None,
        jwt_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        cookie_name: str = "jwt_token",
        cookie_max_age: int = 3600,  # 1 hour
    ) -> None:
        """
        Initialize OAuth router with configuration

        Args:
            prefix (str, optional): URL prefix for routes. Defaults to "/auth".
            tags (list, optional): Route tags for documentation
            dependencies (list, optional): Global route dependencies
            client_id (str, optional): OAuth client ID
            client_secret (str, optional): OAuth client secret
            well_known_config_url (str, optional): Provider's well-known configuration URL
            jwt_secret (str, optional): Secret for JWT token signing
            redirect_uri (str, optional): OAuth callback redirect URI
            cookie_name (str, optional): Name of the JWT cookie
            cookie_max_age (int, optional): Cookie max age in seconds
        """
        # Configuration parameters
        self.client_id = client_id or os.getenv("OAUTH_CLIENT_ID", "")
        self.client_secret = client_secret or os.getenv("OAUTH_CLIENT_SECRET", "")
        self.well_known_config_url = well_known_config_url or os.getenv(
            "OAUTH_WELL_KNOWN_URL", ""
        )
        self.jwt_secret = jwt_secret or os.getenv("JWT_SECRET", "fallback-secret")
        self.redirect_uri = redirect_uri or os.getenv(
            "OAUTH_REDIRECT_URI", f"http://localhost:8000{prefix}/callback"
        )
        self.login_url = f"{prefix}/login"

        # Router configuration
        self.prefix = prefix
        self.tags = tags or ["authentication"]
        self.dependencies = dependencies or []
        self.cookie_name = cookie_name
        self.cookie_max_age = cookie_max_age

        # Initialize router
        self.router = APIRouter(
            prefix=self.prefix, tags=self.tags, dependencies=self.dependencies
        )

        # Fetch OpenID configuration
        self.well_known_configuration_reader = WellKnownConfigurationReader()

        # Register routes
        self._register_routes()

    def _register_routes(self) -> None:
        """
        Register all routes for the OAuth router
        """
        # Login route to initiate OAuth flow
        self.router.add_api_route(
            "/login",
            self.login,
            methods=["GET"],
            summary="Initiate OAuth login",
            description="Redirect to OAuth provider for authentication",
        )

        # Callback route to handle OAuth response
        self.router.add_api_route(
            "/callback",
            self.callback,
            methods=["GET"],
            summary="OAuth callback handler",
            description="Handle OAuth provider callback and set JWT token",
        )

        # Logout route to clear authentication
        self.router.add_api_route(
            "/logout",
            self.logout,
            methods=["GET"],
            summary="Logout user",
            description="Clear authentication token",
        )

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

        return jwt.encode(payload, self.jwt_secret or "", algorithm="HS256")

    def validate_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate JWT token.

        Args:
            token (str): JWT token to validate

        Returns:
            Optional[Dict[str, Any]]: Decoded token payload or None
        """
        assert self.jwt_secret
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            return cast(Dict[str, Any], payload)
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None

    async def login(self, request: Request) -> RedirectResponse:
        """
        Initiate OAuth login process.

        Returns:
            RedirectResponse: Redirect to OAuth provider
        """
        # Generate state for CSRF protection
        state = str(uuid.uuid4())

        # Construct authorization URL
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "openid profile email",
            "state": state,
        }

        assert self.well_known_config_url
        well_known_configuration = (
            self.well_known_configuration_reader.read_from_well_known_configuration(
                well_known_config_url=self.well_known_config_url,
            )
        )
        assert well_known_configuration
        auth_url = (
            f"{well_known_configuration.authorization_endpoint}?{urlencode(params)}"
        )
        logger.info(f"Redirecting to OAuth provider: {auth_url}")

        return RedirectResponse(url=auth_url, status_code=401)

    async def callback(
        self, request: Request, code: str, state: str
    ) -> RedirectResponse:
        """
        Handle OAuth callback and set JWT cookie.

        Args:
            request (Request): Incoming request
            code (str): Authorization code from OAuth provider
            state (str): CSRF state parameter

        Returns:
            RedirectResponse: Redirect after authentication
        """
        assert self.well_known_config_url
        try:
            well_known_configuration = (
                self.well_known_configuration_reader.read_from_well_known_configuration(
                    well_known_config_url=self.well_known_config_url,
                )
            )
            assert well_known_configuration

            # Exchange code for tokens
            token_data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": self.redirect_uri,
            }

            assert well_known_configuration.token_endpoint

            token_response = requests.post(
                well_known_configuration.token_endpoint, data=token_data
            )
            token_response.raise_for_status()
            tokens = token_response.json()

            # Get access token and ID token
            access_token = tokens.get("access_token")

            assert access_token
            assert well_known_configuration.userinfo_endpoint

            # Fetch user info
            headers = {"Authorization": f"Bearer {access_token}"}
            user_response = requests.get(
                well_known_configuration.userinfo_endpoint, headers=headers
            )
            user_response.raise_for_status()
            user_info = user_response.json()

            # Create JWT token
            jwt_token = self.create_jwt_token(user_info)

            # Prepare response with JWT cookie
            response = RedirectResponse(url="/")
            response.set_cookie(
                key=self.cookie_name,
                value=jwt_token,
                httponly=True,
                secure=True,
                samesite="lax",
                max_age=self.cookie_max_age,
            )

            logger.info("Successful OAuth authentication")
            return response

        except requests.RequestException as e:
            logger.error(f"OAuth callback error: {e}")
            raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")

    async def logout(self, request: Request) -> RedirectResponse:
        """
        Logout user by clearing authentication cookie.

        Returns:
            RedirectResponse: Redirect to login page
        """
        response = RedirectResponse(url="/login")
        response.delete_cookie(self.cookie_name)

        logger.info("User logged out")
        return response

    def get_router(self) -> APIRouter:
        """
        Get the configured router

        Returns:
            APIRouter: Configured FastAPI router
        """
        return self.router

    def get_current_user(self, request: Request) -> Optional[Dict[str, Any]]:
        """
        Extract and validate user from JWT token.

        Args:
            request (Request): Incoming HTTP request

        Returns:
            Optional[Dict[str, Any]]: User information or None
        """
        # Check cookie
        token = request.cookies.get(self.cookie_name)

        # Check Authorization header
        if not token:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        # Validate token
        return self.validate_jwt_token(token) if token else None


# Example usage in a FastAPI application
def create_oauth_router() -> OAuthRouter:
    """
    Create an OAuth router with default configuration

    Returns:
        OAuthRouter: Configured OAuth router
    """
    auth_well_known_configuration_uri = os.getenv("AUTH_CONFIGURATION_URI")
    assert auth_well_known_configuration_uri
    return OAuthRouter(
        prefix="/auth",
        well_known_config_url=auth_well_known_configuration_uri,
    )
