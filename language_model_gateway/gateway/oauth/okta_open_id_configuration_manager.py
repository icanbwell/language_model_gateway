import base64

import requests
from typing import Dict, Any, Optional, cast
import jwt


class OktaOpenIDConfigurationManager:
    """
    Manages OpenID Configuration discovery and token validation
    """

    @staticmethod
    def discover_openid_configuration(okta_domain: str) -> Dict[str, Any]:
        """
        Discover OpenID Configuration endpoints

        Args:
            okta_domain (str): Okta organization domain

        Returns:
            Dict[str, Any]: OpenID Configuration metadata
        """
        # Construct well-known OpenID Configuration URL
        well_known_url = f"{okta_domain}/.well-known/openid-configuration"

        try:
            # Fetch OpenID Configuration
            response = requests.get(well_known_url, timeout=10)
            response.raise_for_status()

            # Parse and return configuration
            return cast(Dict[str, Any], response.json())

        except requests.RequestException as e:
            raise ValueError(f"Error discovering OpenID configuration: {e}")

    @staticmethod
    def validate_id_token(
        id_token: str, okta_domain: str, client_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate Okta ID token using OpenID Configuration

        Args:
            id_token (str): Okta ID token
            okta_domain (str): Okta organization domain
            client_id (Optional[str]): Expected client ID

        Returns:
            Dict[str, Any]: Decoded and validated token payload
        """
        try:
            # Discover OpenID Configuration
            config = OktaOpenIDConfigurationManager.discover_openid_configuration(
                okta_domain
            )

            # Fetch JWKS (JSON Web Key Set)
            jwks_uri = config["jwks_uri"]
            jwks_response = requests.get(jwks_uri, timeout=10)
            jwks_response.raise_for_status()
            jwks = jwks_response.json()

            # Prepare validation options
            validation_options = {
                "verify_signature": True,
                "require": ["iss", "sub", "aud", "exp", "iat"],
                "verify_aud": client_id is not None,
            }

            # Validate and decode token
            decoded_token: Dict[str, Any] = jwt.decode(
                id_token,
                jwks,
                algorithms=["RS256"],
                audience=client_id,
                issuer=config["issuer"],
                options=validation_options,
            )

            return decoded_token

        except jwt.PyJWTError as e:
            raise ValueError(f"Token validation failed: {e}")
        except requests.RequestException as e:
            raise ValueError(f"Error fetching JWKS: {e}")

    @staticmethod
    def introspect_token(
        id_token: str,
        okta_domain: str,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Introspect Okta token with flexible authentication

        Args:
            id_token (str): Okta ID token to introspect
            okta_domain (str): Okta organization domain
            client_id (Optional[str]): OAuth client ID
            client_secret (Optional[str]): OAuth client secret

        Returns:
            Dict[str, Any]: Token introspection result
        """
        # Construct introspection endpoint
        introspection_endpoint = f"{okta_domain}/oauth2/v1/introspect"

        # Prepare request data
        data = {"token": id_token, "token_type_hint": "id_token"}

        # Prepare headers
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # Authentication methods
        if client_id and client_secret:
            # Method 1: Basic Authentication with client credentials
            credentials = f"{client_id}:{client_secret}"
            encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode(
                "utf-8"
            )
            headers["Authorization"] = f"Basic {encoded_credentials}"
        elif client_id:
            # Method 2: Client ID as a parameter
            data["client_id"] = client_id

        try:
            # Perform introspection
            response = requests.post(
                introspection_endpoint, headers=headers, data=data, timeout=10
            )

            # Raise exception for bad responses
            response.raise_for_status()

            # Return introspection result
            return cast(Dict[str, Any], response.json())

        except requests.RequestException as e:
            # Detailed error handling
            error_message = f"Introspection failed: {e}"

            # Add response text if available
            if hasattr(e, "response"):
                error_message += f"\nResponse: {e.response.text if e.response else 'No response available'}"

            raise ValueError(error_message)
