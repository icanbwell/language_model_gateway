import json
import logging
import os
from typing import Dict, Any


logger = logging.getLogger(__name__)


class GoogleClientSecretsLoader:
    """Utility class for loading Google client secrets from environment variable."""

    @staticmethod
    def load_client_secrets() -> Dict[str, Any]:
        """
        Load client secrets from environment variable.

        Returns:
            Dict[str, Any]: Parsed client secrets configuration

        Raises:
            ValueError: If environment variable is not set or invalid
        """
        try:
            # Get client secrets from environment variable
            client_secrets_env = os.environ.get("GOOGLE_CLIENT_SECRETS_JSON")

            if not client_secrets_env:
                raise ValueError(
                    "GOOGLE_CLIENT_SECRETS_JSON environment variable is not set"
                )

            # Parse JSON from environment variable
            client_secrets: Dict[str, Any] = json.loads(client_secrets_env)

            # Validate basic structure
            if "installed" not in client_secrets:
                raise ValueError("Invalid client secrets format")

            return client_secrets

        except json.JSONDecodeError:
            raise ValueError(
                "Invalid JSON in GOOGLE_CLIENT_SECRETS_JSON environment variable"
            )
        except Exception as e:
            raise ValueError(f"Error loading client secrets: {str(e)}")
