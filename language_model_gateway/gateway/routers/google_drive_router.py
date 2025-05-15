import dataclasses
import logging
import traceback
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Sequence
from fastapi import params
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse

from language_model_gateway.gateway.oauth.google_drive_authenticator import (
    GoogleDriveAuthenticator,
)

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class ErrorDetail(Dict[str, str]):
    """Structured error detail for consistent error reporting."""

    message: str
    timestamp: str
    trace_id: str
    call_stack: str


class GoogleDriveRouter:
    """Router class for Google Drive authentication and file operations."""

    def __init__(
        self,
        authenticator: GoogleDriveAuthenticator,
        prefix: str = "/api/v1",
        tags: list[str | Enum] | None = None,
        dependencies: Sequence[params.Depends] | None = None,
    ):
        """
        Initialize Google Drive router.

        Args:
            authenticator (GoogleDriveAuthenticator): Authenticator instance
            prefix (str): Router prefix
            tags (Optional[list[str]]): Router tags
            dependencies (Optional[list[Any]]): Router dependencies
        """
        self.authenticator = authenticator
        self.prefix = prefix
        self.tags = tags or ["google-drive"]
        self.dependencies = dependencies or []

        self.router = APIRouter(
            prefix=self.prefix, tags=self.tags, dependencies=self.dependencies
        )

        self._register_routes()

    def _register_routes(self) -> None:
        """Register all routes for this router."""
        self.router.add_api_route(
            "/login",
            self.initiate_google_login,
            methods=["GET"],
            summary="Initiate Google OAuth login",
            description="Start Google OAuth authentication process",
            status_code=302,
        )

        self.router.add_api_route(
            "/callback",
            self.oauth_callback,
            methods=["GET"],
            summary="Handle Google OAuth callback",
            description="Process OAuth callback and exchange code for credentials",
            status_code=200,
        )

    async def initiate_google_login(
        self, okta_token: str, request: Request
    ) -> RedirectResponse:
        """
        Initiate Google OAuth login with Okta token validation.

        Args:
            okta_token (str): Okta JWT token
            request (Request): Incoming request

        Returns:
            RedirectResponse: Redirect to Google authorization URL

        Raises:
            HTTPException: For token validation or other errors
        """
        try:
            # Validate Okta token
            okta_payload = self.authenticator.validate_okta_token(okta_token)

            # Generate authorization URL
            authorization_url = self.authenticator.generate_authorization_url(
                state=okta_payload.get("email")
            )

            return RedirectResponse(url=authorization_url)

        except ValueError as e:
            call_stack = traceback.format_exc()
            error_detail = ErrorDetail(
                message=str(e),
                timestamp=datetime.now().isoformat(),
                trace_id="",
                call_stack=call_stack,
            )
            logger.exception(e, stack_info=True)
            raise HTTPException(status_code=401, detail=error_detail)

        except Exception as e:
            call_stack = traceback.format_exc()
            error_detail = ErrorDetail(
                message="Internal server error during login",
                timestamp=datetime.now().isoformat(),
                trace_id="",
                call_stack=call_stack,
            )
            logger.exception(e, stack_info=True)
            raise HTTPException(status_code=500, detail=error_detail)

    async def oauth_callback(
        self, code: str, state: Optional[str] = None
    ) -> JSONResponse:
        """
        Handle Google OAuth callback.

        Args:
            code (str): Authorization code
            state (Optional[str]): CSRF protection state

        Returns:
            JSONResponse: Authentication result

        Raises:
            HTTPException: For various error conditions
        """
        try:
            # Exchange authorization code for credentials
            credentials = self.authenticator.exchange_authorization_code(code)

            # Optional: Download a file (example)
            file_content = self.authenticator.download_drive_file(
                credentials,
                file_id="your_file_id",  # Replace with actual file ID
            )

            return JSONResponse(
                content={
                    "status": "success",
                    "message": "Authentication completed",
                    "file_size": len(file_content),
                }
            )

        except ValueError as e:
            call_stack = traceback.format_exc()
            error_detail: ErrorDetail = ErrorDetail(
                message=str(e),
                timestamp=datetime.now().isoformat(),
                trace_id="",
                call_stack=call_stack,
            )
            logger.exception(e, stack_info=True)
            raise HTTPException(status_code=400, detail=error_detail)

        except Exception as e:
            call_stack = traceback.format_exc()
            error_detail = ErrorDetail(
                message="Internal server error during callback",
                timestamp=datetime.now().isoformat(),
                trace_id="",
                call_stack=call_stack,
            )
            logger.exception(e, stack_info=True)
            raise HTTPException(status_code=500, detail=error_detail)

    def get_router(self) -> APIRouter:
        """
        Get the configured router.

        Returns:
            APIRouter: Configured FastAPI router
        """
        return self.router
