from typing import Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from language_model_gateway.gateway.oauth.google_client_secrets_loader import (
    GoogleCredentialsManager,
)
from language_model_gateway.gateway.oauth.google_credentials_converter import (
    GoogleCredentialsConverter,
)
from language_model_gateway.gateway.oauth.google_drive_url_parser import (
    GoogleDriveURLParser,
)


class GoogleDriveFileDownloader:
    """
    Utility class for downloading files from Google Drive
    """

    @staticmethod
    def download_file_from_drive(
        file_id: str,
        credentials: Optional[Credentials] = None,
    ) -> bytes:
        """
        Download a file from Google Drive.

        Args:
            file_id (str): Google Drive file ID
            credentials (Optional[Credentials]): Google OAuth credentials

        Returns:
            bytes: File content
        """
        # Get credentials if not provided
        if not credentials:
            credentials = GoogleCredentialsConverter.dict_to_credentials(
                GoogleCredentialsManager().load_credentials()
            )

        # Build Google Drive service
        service = build("drive", "v3", credentials=credentials)

        try:
            # Request file metadata first to verify file exists
            # file_metadata = service.files().get(fileId=file_id).execute()

            # Download file media
            request = service.files().get_media(fileId=file_id)
            file_content: bytes = request.execute()

            return file_content

        except Exception as e:
            raise ValueError(f"Error downloading file: {str(e)}")

    @classmethod
    def download_from_url(
        cls, url: str, credentials: Optional[Credentials] = None
    ) -> bytes:
        """
        Download file directly from a Google Drive sharing URL

        Args:
            url (str): Google Drive sharing URL
            credentials (Optional[Credentials]): Google OAuth credentials

        Returns:
            bytes: File content

        Raises:
            ValueError: If file ID cannot be extracted
        """
        # Extract file ID from URL
        file_id = GoogleDriveURLParser.extract_file_id(url)

        if not file_id:
            raise ValueError(f"Could not extract file ID from URL: {url}")

        # Use existing download method with extracted file ID
        return cls.download_file_from_drive(file_id=file_id, credentials=credentials)
