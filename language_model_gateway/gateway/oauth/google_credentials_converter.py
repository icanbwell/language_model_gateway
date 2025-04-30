from google.oauth2.credentials import Credentials
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class GoogleCredentialsConverter:
    """
    Utility class to convert dictionary to Google OAuth Credentials
    """

    @staticmethod
    def dict_to_credentials(
        credentials_dict: Dict[str, Any], scopes: Optional[list[str]] = None
    ) -> Credentials:
        """
        Convert a dictionary to Google OAuth Credentials.

        Args:
            credentials_dict (Dict[str, Any]): Credentials dictionary
            scopes (Optional[list[str]]): OAuth scopes

        Returns:
            Credentials: Google OAuth Credentials object

        Raises:
            ValueError: If required fields are missing
        """
        # Validate input dictionary
        required_keys = [
            "token",
            "refresh_token",
            "token_uri",
            "client_id",
            "client_secret",
        ]

        for key in required_keys:
            if key not in credentials_dict:
                raise ValueError(f"Missing required key: {key}")

        # Handle optional expiry
        expiry = credentials_dict.get("expiry")
        if not expiry:
            # Default expiry to 1 hour from now if not provided
            expiry = (datetime.utcnow() + timedelta(hours=1)).isoformat()

        # Create Credentials object
        return Credentials(  # type:ignore[no-untyped-call]
            token=credentials_dict["token"],
            refresh_token=credentials_dict["refresh_token"],
            token_uri=credentials_dict["token_uri"],
            client_id=credentials_dict["client_id"],
            client_secret=credentials_dict["client_secret"],
            scopes=scopes or [],
            expiry=datetime.fromisoformat(expiry)
            if isinstance(expiry, str)
            else expiry,
        )

    @staticmethod
    def credentials_to_dict(credentials: Credentials) -> Dict[str, Any]:
        """
        Convert Credentials object to dictionary.

        Args:
            credentials (Credentials): Google OAuth Credentials

        Returns:
            Dict[str, Any]: Credentials as a dictionary
        """
        return {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": list(credentials.scopes),
            "expiry": credentials.expiry.isoformat() if credentials.expiry else None,
        }
