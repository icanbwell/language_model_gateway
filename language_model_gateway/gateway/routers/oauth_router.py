import logging
import os
from enum import Enum
from typing import Optional, Dict, Any, List, Sequence, Annotated, Union

import requests
from fastapi import APIRouter, Request, HTTPException
from fastapi.params import Depends
from fastapi.responses import RedirectResponse

from language_model_gateway.gateway.api_container import (
    get_well_known_configuration_reader,
    get_jwt_authenticator,
)
from language_model_gateway.gateway.utilities.tokens.jwt_authenticator.jwt_authenticator import (
    JwtAuthenticator,
)
from language_model_gateway.gateway.utilities.tokens.jwt_authenticator.oauth_state_store import (
    OAuthStateStore,
)
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
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
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

        # State management
        self.state_store = OAuthStateStore()

        # Initialize router
        self.router = APIRouter(
            prefix=self.prefix, tags=self.tags, dependencies=self.dependencies
        )

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

    async def login(
        self,
        request: Request,
        jwt_authenticator: Annotated[JwtAuthenticator, Depends(get_jwt_authenticator)],
    ) -> RedirectResponse:
        """
        Initiate OAuth login process with CSRF state protection
        """
        assert jwt_authenticator
        assert self.client_id
        assert self.redirect_uri
        assert self.well_known_config_url

        # Generate state for CSRF protection
        state = self.state_store.create_state()

        auth_url = await jwt_authenticator.get_login_url(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            well_known_config_url=self.well_known_config_url,
            state=state,  # Pass state for CSRF protection
        )

        logger.info(f"Redirecting to OAuth provider: {auth_url}")
        return RedirectResponse(url=auth_url, status_code=302)

    async def callback(
        self,
        request: Request,
        code: str,
        state: str,
        well_known_configuration_reader: Annotated[
            WellKnownConfigurationReader, Depends(get_well_known_configuration_reader)
        ],
    ) -> RedirectResponse:
        """
        Handle OAuth callback and set JWT cookie with enhanced security
        """
        assert self.well_known_config_url
        assert well_known_configuration_reader

        # Validate CSRF state
        if not self.state_store.validate_state(state):
            logger.error("Invalid OAuth state - potential CSRF attempt")
            raise HTTPException(status_code=400, detail="Invalid state parameter")

        try:
            well_known_configuration = await well_known_configuration_reader.read_from_well_known_configuration_async(
                well_known_config_url=self.well_known_config_url,
            )
            assert well_known_configuration
            assert well_known_configuration.token_endpoint

            # Exchange code for tokens
            token_data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": self.redirect_uri,
            }

            token_response = requests.post(
                well_known_configuration.token_endpoint, data=token_data
            )
            token_response.raise_for_status()
            tokens = token_response.json()

            # Get access token
            access_token = tokens.get("access_token")
            assert access_token, "No access token received"

            # Prepare response with secure cookie
            response = RedirectResponse(url="/")
            response.set_cookie(
                key=self.cookie_name,
                value=access_token,
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
        except AssertionError as e:
            logger.error(f"Token validation error: {e}")
            raise HTTPException(status_code=400, detail="Invalid token response")

    async def logout(self, request: Request) -> RedirectResponse:
        """
        Logout user by clearing authentication cookie
        """
        response = RedirectResponse(url="/login")
        response.delete_cookie(self.cookie_name)

        logger.info("User logged out")
        return response

    def get_router(self) -> APIRouter:
        """
        Get the configured router
        """
        return self.router

    def get_current_user(
        self,
        *,
        request: Request,
        jwt_authenticator: JwtAuthenticator,
    ) -> Optional[Dict[str, Any]]:
        """
        Extract and validate user from JWT token
        """
        assert self.jwt_secret

        # Check cookie
        token = request.cookies.get(self.cookie_name)

        # Check Authorization header
        if not token:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        # Validate token
        return (
            jwt_authenticator.validate_jwt_token(
                token=token, jwt_secret=self.jwt_secret
            )
            if token
            else None
        )


def create_oauth_router() -> OAuthRouter:
    """
    Create an OAuth router with default configuration
    """
    auth_well_known_configuration_uri = os.getenv("AUTH_CONFIGURATION_URI")
    assert auth_well_known_configuration_uri, "AUTH_CONFIGURATION_URI must be set"

    return OAuthRouter(
        prefix="/auth",
        well_known_config_url=auth_well_known_configuration_uri,
    )
