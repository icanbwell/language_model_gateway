import dataclasses


@dataclasses.dataclass
class WellKnownConfiguration:
    authorization_endpoint: str | None
    token_endpoint: str | None
    userinfo_endpoint: str | None
    jwks_uri: str | None
    issuer: str | None
    end_session_endpoint: str | None
    scopes_supported: list[str] | None
    response_types_supported: list[str] | None
    token_endpoint_auth_methods_supported: list[str] | None
    revocation_endpoint: str | None
    introspection_endpoint: str | None
