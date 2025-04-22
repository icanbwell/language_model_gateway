import typing
from typing import (
    Optional,
    Any,
    Sequence,
    Union,
    Callable,
    AsyncIterator,
    List,
    Iterator,
)

from langchain_core.callbacks import (
    CallbackManagerForLLMRun,
    AsyncCallbackManagerForLLMRun,
)
from langchain_core.language_models import BaseChatModel, LanguageModelInput
from langchain_core.messages import BaseMessage, AIMessage, AIMessageChunk
from langchain_core.outputs import ChatResult, ChatGenerationChunk, ChatGeneration
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool

from tests.gateway.mocks.mock_ai_message_protocol import MockAiMessageProtocol


class MockChatModel(BaseChatModel):
    fn_get_response: MockAiMessageProtocol

    @property
    def _llm_type(self) -> str:
        return "mock"

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        content: str = self.fn_get_response(messages=messages)
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content=content))]
        )

    async def _agenerate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        content: str = self.fn_get_response(messages=messages)
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content=content))]
        )

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        content: str = self.fn_get_response(messages=messages)
        return iter(
            [
                ChatGenerationChunk(
                    message=AIMessageChunk(
                        content=[{"type": "text", "text": content, "index": 0}],
                        id="run-da3c2606-4792-440a-ac66-72e0d1f6d117",
                    )
                )
            ]
        )

    async def _astream(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        content: str = self.fn_get_response(messages=messages)

        # Split content into words to simulate streaming
        words = content.split()

        for i, word in enumerate(words):
            yield ChatGenerationChunk(
                message=AIMessageChunk(
                    content=[{"type": "text", "text": word + " ", "index": i}],
                    id="run-da3c2606-4792-440a-ac66-72e0d1f6d117",
                )
            )

    def bind_tools(
        self,
        tools: Sequence[
            Union[typing.Dict[str, Any], type, Callable[[], Any], BaseTool]  # noqa: UP006
        ],
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, BaseMessage]:
        return self
