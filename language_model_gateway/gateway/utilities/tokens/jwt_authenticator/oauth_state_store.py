import secrets
from typing import Dict


class OAuthStateStore:
    """
    Simple in-memory state management for CSRF protection
    Note: In production, use a distributed cache like Redis
    """

    def __init__(self) -> None:
        self._states: Dict[str, str] = {}

    def create_state(self) -> str:
        """Generate a unique state for CSRF protection"""
        state = secrets.token_urlsafe(32)
        self._states[state] = state
        return state

    def validate_state(self, state: str) -> bool:
        """Validate and consume the state"""
        if state in self._states:
            del self._states[state]
            return True
        return False
