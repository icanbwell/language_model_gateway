import io
import logging
from typing import Dict, Any, Optional, cast
import jwt

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import Flow

from language_model_gateway.gateway.oauth.google_client_secrets_loader import (
    GoogleCredentialsManager,
)
from language_model_gateway.gateway.oauth.google_credentials_converter import (
    GoogleCredentialsConverter,
)

logger = logging.getLogger(__name__)


class GoogleDriveAuthenticator:
    """Authenticator for Google Drive operations."""

    def __init__(self, redirect_uri: str, scopes: Optional[list[str]] = None):
        """
        Initialize Google Drive authenticator.

        Args:
            redirect_uri (str): OAuth redirect URI
            scopes (Optional[list[str]]): OAuth scopes
        """
        self.client_secrets: Credentials = (
            GoogleCredentialsConverter.dict_to_credentials(
                GoogleCredentialsManager.load_credentials()
            )
        )
        self.redirect_uri = redirect_uri
        self.scopes = scopes or [
            "https://www.googleapis.com/auth/drive.readonly",
            "openid",
            "email",
        ]

    # noinspection PyMethodMayBeStatic
    def validate_okta_token(self, okta_token: str) -> Dict[str, Any]:
        """
        Validate Okta JWT token.

        Args:
            okta_token (str): Okta JWT token

        Returns:
            Dict[str, Any]: Decoded token payload

        Raises:
            ValueError: If token is invalid
        """
        try:
            # Decode without signature verification (add proper verification in production)
            decoded_token: Dict[str, Any] = jwt.decode(
                okta_token, options={"verify_signature": False}
            )

            # Basic validation
            if not decoded_token.get("email"):
                raise ValueError("Token missing email")

            return decoded_token

        except jwt.PyJWTError as e:
            raise ValueError(f"Token validation failed: {str(e)}")

    def create_oauth_flow(self) -> Flow:
        """
        Create Google OAuth flow.

        Returns:
            Flow: Configured OAuth flow
        """
        # Use in-memory client secrets instead of file path
        flow = Flow.from_client_config(
            client_config=self.client_secrets,
            scopes=self.scopes,
            redirect_uri=self.redirect_uri,
        )
        return flow

    def generate_authorization_url(self, state: Optional[str] = None) -> str:
        """
        Generate Google OAuth authorization URL.

        Args:
            state (Optional[str]): CSRF protection state

        Returns:
            str: Authorization URL
        """
        flow = self.create_oauth_flow()

        authorization_url: str
        authorization_url, _ = flow.authorization_url(
            access_type="offline", prompt="consent", state=state
        )

        return authorization_url

    def exchange_authorization_code(self, authorization_code: str) -> Credentials:
        """
        Exchange authorization code for Google credentials.

        Args:
            authorization_code (str): OAuth authorization code

        Returns:
            Credentials: Google OAuth credentials
        """
        flow: Flow = self.create_oauth_flow()
        flow.fetch_token(code=authorization_code)
        return cast(Credentials, flow.credentials)

    # noinspection PyMethodMayBeStatic
    def download_drive_file(self, credentials: Credentials, file_id: str) -> bytes:
        """
        Download file from Google Drive.

        Args:
            credentials (Credentials): Google OAuth credentials
            file_id (str): Google Drive file ID

        Returns:
            bytes: File content

        Raises:
            ValueError: If file download fails
        """
        try:
            # Build Google Drive service
            service = build("drive", "v3", credentials=credentials)

            # Download file
            request = service.files().get_media(fileId=file_id)

            file_bytes = io.BytesIO()
            downloader = MediaIoBaseDownload(file_bytes, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

            file_bytes.seek(0)
            return file_bytes.read()

        except Exception as e:
            raise ValueError(f"File download error: {str(e)}")
