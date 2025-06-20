import os
import requests
from typing import Optional, Dict, Any
import jwt
import logging


class OktaTokenExchanger:
    def __init__(
        self,
        okta_domain: str,
        client_id: str,
        client_secret: str,
        scopes: Optional[list[str]] = None,
    ):
        """
        Initialize Okta Token Exchanger.

        Args:
            okta_domain (str): Okta organization domain
            client_id (str): Okta OAuth client ID
            scopes (Optional[list[str]]): OAuth scopes to request
        """
        # Ensure domain is properly formatted
        self.okta_domain = okta_domain.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret

        # Default scopes with offline_access for refresh token
        self.scopes = scopes or ["openid", "profile", "email", "offline_access"]

        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def validate_id_token(self, id_token: str) -> Optional[Dict[str, Any]]:
        """
        Validate the structure and basic properties of the ID token.

        Args:
            id_token (str): Okta ID token

        Returns:
            Decoded token payload or None if invalid
        """
        try:
            # Decode without signature verification
            decoded = jwt.decode(
                id_token,
                options={
                    "verify_signature": False,
                    "verify_aud": False,
                    "verify_iat": False,
                },
            )

            # Additional validation checks
            if not decoded:
                self.logger.error("Token decoding returned empty payload")
                return None

            # Check for required claims
            required_claims = ["sub", "iss", "aud"]
            for claim in required_claims:
                if claim not in decoded:
                    self.logger.error(f"Missing required claim: {claim}")
                    return None

            return decoded

        except jwt.PyJWTError as e:
            self.logger.error(f"JWT Decoding error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error validating ID token: {e}")
            return None

    def exchange_for_tokens(self, id_token: str) -> Optional[Dict[str, Any]]:
        """
        Exchange ID token for a new set of tokens including refresh token.

        Args:
            id_token (str): Okta ID token

        Returns:
            Dict of tokens or None if exchange fails
        """
        # Validate ID token first
        decoded_token = self.validate_id_token(id_token)
        if not decoded_token:
            self.logger.error("ID token validation failed")
            return None

        # Construct token exchange endpoint
        token_endpoint = f"{self.okta_domain}/oauth2/v1/token"

        # Prepare token exchange payload
        payload = {
            # 'grant_type': 'urn:okta:params:oauth:grant-type:token-exchange',
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "subject_token": id_token,
            "subject_token_type": "urn:ietf:params:oauth:token-type:id_token",
            "requested_token_type": "urn:ietf:params:oauth:token-type:refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": " ".join(self.scopes),
        }

        try:
            # Perform token exchange with enhanced error handling
            response = requests.post(
                token_endpoint,
                data=payload,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                timeout=10,  # Add timeout to prevent hanging
            )

            # Detailed error logging
            if response.status_code != 200:
                self.logger.error(
                    f"Token exchange failed with status {response.status_code}"
                )
                self.logger.error(f"Response body: {response.text}")
                return None

            # Parse token response
            token_response = response.json()

            # Validate token response
            required_tokens = ["access_token", "refresh_token"]
            for token_type in required_tokens:
                if token_type not in token_response:
                    self.logger.error(f"Missing {token_type} in response")
                    return None

            return {
                "access_token": token_response["access_token"],
                "refresh_token": token_response["refresh_token"],
                "id_token": token_response.get("id_token"),
            }

        except requests.RequestException as e:
            self.logger.error(f"Token exchange request error: {e}")
            return None
        except ValueError as e:
            self.logger.error(f"JSON parsing error: {e}")
            return None


def test_okta_token_refresh():
    # Configuration validation with comprehensive checks
    try:
        OKTA_DOMAIN = os.environ.get("OKTA_DOMAIN")
        CLIENT_ID = os.environ.get("OKTA_CLIENT_ID")
        CLIENT_SECRET = os.environ.get("OKTA_CLIENT_SECRET")
        ID_TOKEN = os.environ.get("OKTA_ID_TOKEN")

        # Comprehensive input validation
        if not all([OKTA_DOMAIN, CLIENT_ID, ID_TOKEN]):
            raise ValueError("Missing required environment variables")

        # Validate domain format
        if not OKTA_DOMAIN.startswith("https://"):
            OKTA_DOMAIN = f"https://{OKTA_DOMAIN}"

        # Initialize token exchanger
        token_exchanger = OktaTokenExchanger(
            okta_domain=OKTA_DOMAIN, client_id=CLIENT_ID, client_secret=CLIENT_SECRET
        )

        # Attempt token exchange
        new_tokens = token_exchanger.exchange_for_tokens(ID_TOKEN)

        if new_tokens:
            print("Token Exchange Successful")
            print("Access Token Available:", bool(new_tokens.get("access_token")))
            print("Refresh Token Available:", bool(new_tokens.get("refresh_token")))
        else:
            print("Token exchange failed")

    except Exception as e:
        print(f"Critical error in token exchange: {e}")
        import traceback

        traceback.print_exc()
