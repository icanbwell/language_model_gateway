from typing import Protocol, Dict, Any

from language_model_gateway.configs.config_schema import ChatModelConfig
from language_model_gateway.gateway.schema.openai.completions import ChatRequest


class MockChatResponseProtocol(Protocol):
    def __call__(
        self,
        *,
        model_config: ChatModelConfig,
        headers: Dict[str, str],
        chat_request: ChatRequest,
    ) -> Dict[str, Any]: ...
