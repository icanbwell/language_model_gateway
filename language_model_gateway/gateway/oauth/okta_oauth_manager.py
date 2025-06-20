import os
import requests
from typing import Dict, Any
from urllib.parse import urlencode


class OktaOAuthManager:
    def __init__(
        self, okta_domain: str, client_id: str, client_secret: str, redirect_uri: str
    ):
        """
        Initialize Okta OAuth Manager.

        Args:
            okta_domain (str): Okta organization domain
            client_id (str): Okta OAuth client ID
            client_secret (str): Okta OAuth client secret
            redirect_uri (str): Registered redirect URI
        """
        self.okta_domain = okta_domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def generate_authorization_url(self, scopes: list[str]) -> str:
        """
        Generate Okta authorization URL.

        Args:
            scopes (list[str]): List of OAuth scopes to request

        Returns:
            str: Authorization URL
        """
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "scope": " ".join(scopes),
            "redirect_uri": self.redirect_uri,
            "state": os.urandom(16).hex(),  # CSRF protection
        }

        authorization_endpoint = f"{self.okta_domain}/oauth2/v1/authorize"
        return f"{authorization_endpoint}?{urlencode(params)}"

    def exchange_code_for_tokens(self, authorization_code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for tokens.

        Args:
            authorization_code (str): Authorization code from Okta

        Returns:
            Dict[str, Any]: Token response
        """
        token_endpoint = f"{self.okta_domain}/oauth2/v1/token"

        payload = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = requests.post(token_endpoint, data=payload)

        if response.status_code != 200:
            raise ValueError(f"Token exchange failed: {response.text}")

        return response.json()

    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh access token using refresh token.

        Args:
            refresh_token (str): Refresh token

        Returns:
            Dict[str, Any]: New token response
        """
        token_endpoint = f"{self.okta_domain}/oauth2/v1/token"

        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = requests.post(token_endpoint, data=payload)

        if response.status_code != 200:
            raise ValueError(f"Token refresh failed: {response.text}")

        return response.json()


def main():
    # Configuration (typically from environment or secure config)
    OKTA_DOMAIN = os.getenv("OKTA_DOMAIN")
    CLIENT_ID = os.getenv("OKTA_CLIENT_ID")
    CLIENT_SECRET = os.getenv("OKTA_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("OKTA_REDIRECT_URI")

    # Recommended scopes for Google Drive access
    SCOPES = [
        "openid",  # Required for ID token
        "profile",  # User profile information
        "email",  # Email access
        "offline_access",  # Critical for obtaining refresh token
    ]

    # Initialize OAuth Manager
    okta_oauth = OktaOAuthManager(
        okta_domain=OKTA_DOMAIN,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
    )

    # Step 1: Generate Authorization URL (to be used in browser/redirect)
    authorization_url = okta_oauth.generate_authorization_url(SCOPES)
    print("Please visit this URL and authorize the application:")
    print(authorization_url)

    # Step 2: Manually input the authorization code received after user consent
    authorization_code = input("Enter the authorization code: ")

    # Step 3: Exchange code for tokens
    token_response = okta_oauth.exchange_code_for_tokens(authorization_code)

    # Extract and store tokens securely
    id_token = token_response.get("id_token")
    access_token = token_response.get("access_token")
    refresh_token = token_response.get("refresh_token")

    # Optional: Demonstrate token refresh
    if refresh_token:
        new_token_response = okta_oauth.refresh_access_token(refresh_token)
        print("New access token obtained")


if __name__ == "__main__":
    main()
