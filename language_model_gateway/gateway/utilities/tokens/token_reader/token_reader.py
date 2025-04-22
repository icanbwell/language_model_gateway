from typing import Dict, Any, Optional, List, cast
import jwt
import requests
from jwt.algorithms import RSAAlgorithm
from cryptography.hazmat.primitives.asymmetric import rsa
import json
import time


class OpenIDTokenValidator:
    def __init__(
        self,
        well_known_config_url: str,
        audience: Optional[str] = None,
        issuer: Optional[str] = None,
    ):
        """
        Initialize OpenID Connect token validator.

        Args:
            well_known_config_url (str): URL of the OpenID provider's well-known configuration
            audience (Optional[str]): Expected audience of the token
            issuer (Optional[str]): Expected issuer of the token
        """
        self._well_known_config_url = well_known_config_url
        self._audience = audience
        self._issuer = issuer

        # Cached configuration and keys
        self._config: Dict[str, Any] = {}
        self._jwks_keys: List[Dict[str, str]] = []
        self._last_key_fetch_time = 0

        # Fetch initial configuration
        self._fetch_configuration()

    def _fetch_configuration(self) -> None:
        """
        Fetch OpenID provider configuration from well-known URL.

        Raises:
            ValueError: If configuration cannot be retrieved
        """
        try:
            response = requests.get(self._well_known_config_url)
            response.raise_for_status()
            self._config = response.json()

            # Fetch JWKS keys
            jwks_url = self._config.get("jwks_uri")
            if not jwks_url:
                raise ValueError("No JWKS URI found in configuration")

            jwks_response = requests.get(jwks_url)
            jwks_response.raise_for_status()
            self._jwks_keys = jwks_response.json().get("keys", [])

            self._last_key_fetch_time = int(time.time())

        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch OpenID configuration: {e}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON in OpenID configuration")

    def _get_public_key(self, token_header: Dict[str, str]) -> rsa.RSAPublicKey:
        """
        Retrieve the appropriate public key for token verification.

        Args:
            token_header (Dict[str, str]): Decoded token header

        Returns:
            rsa.RSAPublicKey: Public key for signature verification

        Raises:
            ValueError: If no matching key is found
        """
        # Refresh keys if they're older than 1 hour
        if time.time() - self._last_key_fetch_time > 3600:
            self._fetch_configuration()

        kid = token_header.get("kid")

        for jwk in self._jwks_keys:
            if jwk.get("kid") == kid:
                # Convert JWK to RSA public key
                public_numbers = RSAAlgorithm.from_jwk(json.dumps(jwk))
                return cast(rsa.RSAPublicKey, public_numbers)

        raise ValueError("No matching public key found")

    def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Validate and decode an OpenID Connect JWT token.

        Args:
            token (str): JWT token to validate

        Returns:
            Dict[str, Any]: Decoded and validated token payload

        Raises:
            ValueError: For various token validation failures
        """
        try:
            # Decode header without verification to get key ID
            unverified_header = jwt.get_unverified_header(token)

            # Get public key
            public_key = self._get_public_key(unverified_header)

            # Full token validation
            payload = jwt.decode(
                token,
                public_key or "",
                algorithms=["RS256"],
                options={
                    "verify_signature": True,
                    "require_exp": True,
                    "verify_exp": True,
                    "verify_aud": self._audience is not None,
                    "verify_iss": self._issuer is not None,
                },
            )

            # Additional custom validations
            if self._audience and payload.get("aud") != self._audience:
                raise ValueError("Invalid token audience")

            if self._issuer and payload.get("iss") != self._issuer:
                raise ValueError("Invalid token issuer")

            return cast(Dict[str, Any], payload)

        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Token validation failed: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected error during token validation: {e}")
