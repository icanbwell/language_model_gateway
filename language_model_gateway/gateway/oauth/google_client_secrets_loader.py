import json
import logging
import os
from typing import Dict, Any


logger = logging.getLogger(__name__)


class GoogleCredentialsManager:
    """
    Manages Google Drive credentials stored in environment variables
    """

    ENV_VAR_NAME = "GOOGLE_CREDENTIALS_JSON"

    @classmethod
    def load_credentials(cls) -> Dict[str, Any]:
        """
        Load Google credentials from environment variable.

        Returns:
            Dict[str, Any]: Parsed credentials

        Raises:
            ValueError: If credentials are not properly set
        """
        # Retrieve credentials from environment variable
        credentials_str = os.environ.get(cls.ENV_VAR_NAME)

        if not credentials_str:
            raise ValueError(f"Environment variable {cls.ENV_VAR_NAME} is not set")

        try:
            # Try direct JSON parsing first
            credentials: Dict[str, Any] = json.loads(credentials_str)
        except json.JSONDecodeError:
            try:
                # Try base64 decoding
                credentials = json.loads(credentials_str).decode("utf-8")

            except Exception:
                raise ValueError(
                    "Invalid credentials format. Must be valid JSON or base64 encoded JSON"
                )

        # Validate basic structure
        cls._validate_credentials(credentials)

        return credentials

    @classmethod
    def _validate_credentials(cls, credentials: Dict[str, Any]) -> None:
        """
        Validate the structure of credentials.

        Args:
            credentials (Dict[str, Any]): Credentials to validate

        Raises:
            ValueError: If credentials are invalid
        """
        required_keys = ["installed", "client_id", "client_secret", "project_id"]

        # Check for top-level 'installed' key
        if "installed" not in credentials:
            raise ValueError("Credentials must have an 'installed' top-level key")

        # Check for required keys in 'installed'
        installed = credentials["installed"]
        for key in required_keys[1:]:
            if key not in installed:
                raise ValueError(f"Missing required key: {key}")

    @classmethod
    def encode_credentials(cls, credentials_dict: Dict[str, Any]) -> str:
        """
        Encode credentials to base64 for secure storage.

        Args:
            credentials_dict (Dict[str, Any]): Credentials to encode

        Returns:
            str: Base64 encoded credentials
        """
        # Validate credentials before encoding
        cls._validate_credentials(credentials_dict)

        # Convert to JSON string
        credentials_json = json.dumps(credentials_dict)

        # Encode to base64
        return credentials_json
