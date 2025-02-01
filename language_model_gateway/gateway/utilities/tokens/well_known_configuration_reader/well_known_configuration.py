import dataclasses


@dataclasses.dataclass
class WellKnownConfiguration:
    authorization_endpoint: str | None
    token_endpoint: str | None
    userinfo_endpoint: str | None
