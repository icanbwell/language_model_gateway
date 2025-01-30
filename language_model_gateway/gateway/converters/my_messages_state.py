from typing import Optional

from langchain_core.messages.ai import UsageMetadata
from langgraph.prebuilt.chat_agent_executor import AgentState


class MyMessagesState(AgentState):
    usage_metadata: Optional[UsageMetadata]
