from typing import Dict, Any, Optional

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    ToolMessage,
    SystemMessage,
)
from langchain_core.messages import (
    ChatMessage as LangchainChatMessage,
)
from openai.types.chat import ChatCompletionMessage


def convert_message_content_to_string(content: str | list[str | Dict[str, Any]]) -> str:
    if isinstance(content, str):
        return content
    text: list[str] = []
    for content_item in content:
        if isinstance(content_item, str):
            text.append(content_item)
        elif isinstance(content_item, dict):
            content_item_type: Optional[str] = content_item.get("type")
            if content_item_type == "text":
                text.append(content_item.get("text") or "")
        else:
            assert (
                False
            ), f"Unsupported content item type: {type(content_item)}: {content_item}"
    return "".join(text)


def langchain_to_chat_message(message: BaseMessage) -> Optional[ChatCompletionMessage]:
    """Create a ChatMessage from a LangChain message."""
    match message:
        case SystemMessage():
            assert (
                False
            ), "System messages should not be converted to ChatCompletionMessage"
        case HumanMessage():
            assert (
                False
            ), "Human messages should not be converted to ChatCompletionMessage"
        case AIMessage():
            ai_message = ChatCompletionMessage(
                role="assistant",
                content=convert_message_content_to_string(message.content),
            )
            # if message.tool_calls:
            #     ai_message.tool_calls = message.tool_calls
            # if message.response_metadata:
            #     ai_message.response_metadata = message.response_metadata
            return ai_message
        case ToolMessage():
            # content: str = convert_message_content_to_string(message.content)
            artifact: str = message.artifact
            if artifact:
                ai_message = ChatCompletionMessage(
                    role="assistant",
                    content=artifact,
                )
                return ai_message
        case LangchainChatMessage():
            assert (
                False
            ), "Chat messages should not be converted to ChatCompletionMessage"
        case _:
            raise ValueError(f"Unsupported message type: {message.__class__.__name__}")
    return None


def remove_tool_calls(
    content: str | list[str | dict[str, Any]]
) -> str | list[str | dict[str, Any]]:
    """Remove tool calls from content."""
    if isinstance(content, str):
        return content
    # Currently only Anthropic models stream tool calls, using content item type tool_use.
    return [
        content_item
        for content_item in content
        if isinstance(content_item, str) or content_item["type"] != "tool_use"
    ]
