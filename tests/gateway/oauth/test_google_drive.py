import os
from typing import Optional, Dict, Any, cast

import jwt
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from jwt.algorithms import RSAAlgorithm
from googleapiclient.discovery import build
from language_model_gateway.gateway.oauth.google_client_secrets_loader import (
    GoogleCredentialsManager,
)


class OktaGoogleDriveIntegration:
    def __init__(
        self,
        *,
        okta_id_token: str,
        google_client_id: str,
        okta_domain: str,
        okta_audience_id: Optional[str] = None,
    ) -> None:
        """
        Initialize the Google Drive access using Okta ID token.

        Args:
            okta_id_token (str): The ID token from Okta
            google_client_id (str): The Google OAuth client ID
            okta_domain (str): Your Okta domain (e.g., 'https://your-org.okta.com')
        """
        self.okta_id_token = okta_id_token
        self.google_client_id = google_client_id
        self.okta_domain = okta_domain
        self.okta_audience_id = okta_audience_id
        self.jwks_cache: Optional[Dict[str, Any]] = None

    def _fetch_jwks(self) -> Optional[Dict[str, Any]]:
        """
        Fetch JWKS (JSON Web Key Set) from Okta.

        Returns:
            Dictionary of JWKS or None if fetch fails
        """
        try:
            # Construct JWKS endpoint URL
            jwks_url = f"{self.okta_domain}/oauth2/v1/keys"

            # Fetch JWKS with proper error handling
            response = requests.get(jwks_url, timeout=10)
            response.raise_for_status()

            return cast(Dict[str, Any], response.json())
        except requests.RequestException as e:
            print(f"JWKS Fetch Error: {e}")
            return None

    def validate_okta_token(self) -> Optional[Dict[str, Any]]:
        """
        Validate the Okta ID token using manual JWKS verification.

        Returns:
            Decoded token claims if valid, None otherwise
        """
        try:
            # Fetch JWKS if not cached
            if not self.jwks_cache:
                self.jwks_cache = self._fetch_jwks()

            if not self.jwks_cache:
                print("Could not retrieve JWKS")
                return None

            # Decode token headers to get key ID
            unverified_headers = jwt.get_unverified_header(self.okta_id_token)
            kid = unverified_headers.get("kid")

            # Find matching key in JWKS
            matching_key = None
            for key in self.jwks_cache.get("keys", []):
                if key.get("kid") == kid:
                    matching_key = key
                    break

            if not matching_key:
                print(f"No matching key found for kid: {kid}")
                return None

            # Convert JWKS key to public key
            public_key = RSAAlgorithm.from_jwk(matching_key)

            # Verify token with additional checks
            decoded_token: Dict[str, Any] = jwt.decode(
                self.okta_id_token,
                key=public_key,  # type:ignore[arg-type]
                algorithms=["RS256"],
                audience=self.okta_audience_id,
                issuer=f"{self.okta_domain}",
            )

            return decoded_token

        except jwt.PyJWTError as e:
            print(f"Token Validation Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected Error during token validation: {e}")
            return None

    def exchange_token_for_google_credentials(self) -> Optional[Credentials]:
        """
        Exchange Okta ID token for Google Drive credentials.

        Returns:
            Google credentials or None if exchange fails
        """
        token_info = self.validate_okta_token()
        if not token_info:
            return None

        try:
            credentials_dict = GoogleCredentialsManager.load_credentials()
            # Create credentials from the Okta token
            credentials = Credentials(  # type:ignore[no-untyped-call]
                token=self.okta_id_token,
                token_uri=credentials_dict["web"]["token_uri"],
                client_id=credentials_dict["web"]["client_id"],
                client_secret=credentials_dict["web"]["client_secret"],
            )

            credentials.refresh(Request())  # type:ignore[no-untyped-call]

            return credentials
        except Exception as e:
            print(f"Credential exchange error: {e}")
            return None

    def get_google_drive_service(self) -> Optional[Any]:
        """
        Get Google Drive service using the exchanged credentials.

        Returns:
            Google Drive service object or None
        """
        credentials = self.exchange_token_for_google_credentials()
        if not credentials:
            return None

        try:
            # Build and return the Google Drive service
            return build("drive", "v3", credentials=credentials)
        except Exception as e:
            print(f"Google Drive service creation error: {e}")
            return None

    def list_drive_files(self, max_results: int = 10) -> Optional[list[Any]]:
        """
        List files in the user's Google Drive.

        Args:
            max_results (int): Maximum number of files to retrieve

        Returns:
            List of files or None if retrieval fails
        """
        drive_service = self.get_google_drive_service()
        if not drive_service:
            return None

        try:
            # Retrieve files from Google Drive
            results = (
                drive_service.files()
                .list(
                    pageSize=max_results,
                    fields="nextPageToken, files(id, name, mimeType)",
                )
                .execute()
            )

            return cast(list[Any], results.get("files", []))
        except Exception as e:
            print(f"Error retrieving drive files: {e}")
            return None


# Example usage
def main() -> None:
    # Replace with your actual values
    OKTA_ID_TOKEN = os.getenv("OKTA_ID_TOKEN")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    OKTA_DOMAIN = os.getenv("OKTA_ORG_URL")
    OKTA_AUDIENCE_ID = os.getenv("OKTA_AUDIENCE_ID")

    assert OKTA_ID_TOKEN
    assert GOOGLE_CLIENT_ID
    assert OKTA_DOMAIN
    assert OKTA_AUDIENCE_ID

    # Create integration instance
    drive_integration = OktaGoogleDriveIntegration(
        okta_id_token=OKTA_ID_TOKEN,
        google_client_id=GOOGLE_CLIENT_ID,
        okta_domain=OKTA_DOMAIN,
        okta_audience_id=OKTA_AUDIENCE_ID,
    )

    # Validate and list drive files
    files = drive_integration.list_drive_files()
    if files:
        for file in files:
            print(f"File Name: {file['name']}, Type: {file['mimeType']}")
    else:
        print("Could not retrieve files")


if __name__ == "__main__":
    main()
