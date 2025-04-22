import datetime
import random
from typing import Dict, Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.graph.state import CompiledStateGraph
from starlette.responses import StreamingResponse, JSONResponse

from language_model_gateway.configs.config_schema import ChatModelConfig
from language_model_gateway.gateway.converters.langgraph_to_openai_converter import (
    LangGraphToOpenAIConverter,
)
from language_model_gateway.gateway.models.model_factory import ModelFactory
from language_model_gateway.gateway.providers.base_chat_completions_provider import (
    BaseChatCompletionsProvider,
)
from language_model_gateway.gateway.schema.openai.completions import ChatRequest
from language_model_gateway.gateway.tools.tool_provider import ToolProvider


class LangChainCompletionsProvider(BaseChatCompletionsProvider):
    def __init__(
        self,
        *,
        model_factory: ModelFactory,
        lang_graph_to_open_ai_converter: LangGraphToOpenAIConverter,
        tool_provider: ToolProvider,
    ) -> None:
        self.model_factory: ModelFactory = model_factory
        assert self.model_factory is not None
        assert isinstance(self.model_factory, ModelFactory)
        self.lang_graph_to_open_ai_converter: LangGraphToOpenAIConverter = (
            lang_graph_to_open_ai_converter
        )
        assert self.lang_graph_to_open_ai_converter is not None
        assert isinstance(
            self.lang_graph_to_open_ai_converter, LangGraphToOpenAIConverter
        )
        self.tool_provider: ToolProvider = tool_provider
        assert self.tool_provider is not None
        assert isinstance(self.tool_provider, ToolProvider)

    async def chat_completions(
        self,
        *,
        model_config: ChatModelConfig,
        headers: Dict[str, str],
        chat_request: ChatRequest,
    ) -> StreamingResponse | JSONResponse:
        # noinspection PyArgumentList
        llm: BaseChatModel = self.model_factory.get_model(
            chat_model_config=model_config
        )

        # noinspection PyUnusedLocal
        def get_current_time(*args: Any, **kwargs: Any) -> str:
            """Returns the current time in H:MM AM/PM format."""
            now = datetime.datetime.now()  # Get current time
            return now.strftime("%Y-%m-%d %H:%M:%S%Z%z")

        # Initialize tools
        tools: Sequence[BaseTool] = (
            self.tool_provider.get_tools(tools=[t for t in model_config.get_agents()])
            if model_config.get_agents() is not None
            else []
        )

        compiled_state_graph: CompiledStateGraph = (
            await self.lang_graph_to_open_ai_converter.create_graph_for_llm_async(
                llm=llm,
                tools=tools,
            )
        )
        request_id = random.randint(1, 1000)

        return await self.lang_graph_to_open_ai_converter.call_agent_with_input(
            request_id=str(request_id),
            headers=headers,
            compiled_state_graph=compiled_state_graph,
            chat_request=chat_request,
            system_messages=[],
        )
