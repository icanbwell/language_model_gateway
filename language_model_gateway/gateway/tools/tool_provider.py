from os import environ
from typing import Dict

from langchain_community.tools import (
    DuckDuckGoSearchRun,
    ArxivQueryRun,
)
from langchain_core.tools import BaseTool

from language_model_gateway.configs.config_schema import ToolConfig
from language_model_gateway.gateway.file_managers.file_manager_factory import (
    FileManagerFactory,
)
from language_model_gateway.gateway.image_generation.image_generator_factory import (
    ImageGeneratorFactory,
)
from language_model_gateway.gateway.tools.current_time_tool import CurrentTimeTool
from langchain_community.tools.pubmed.tool import PubmedQueryRun

from language_model_gateway.gateway.tools.er_diagram_generator_tool import (
    ERDiagramGeneratorTool,
)
from language_model_gateway.gateway.tools.flow_chart_generator_tool import (
    FlowChartGeneratorTool,
)
from language_model_gateway.gateway.tools.google_search_tool import GoogleSearchTool
from language_model_gateway.gateway.tools.graph_viz_diagram_generator_tool import (
    GraphVizDiagramGeneratorTool,
)
from language_model_gateway.gateway.tools.image_generator_tool import ImageGeneratorTool
from language_model_gateway.gateway.tools.network_topology_diagram_tool import (
    NetworkTopologyGeneratorTool,
)
from language_model_gateway.gateway.tools.provider_search_tool import ProviderSearchTool
from language_model_gateway.gateway.tools.python_repl_tool import PythonReplTool
from language_model_gateway.gateway.tools.scraping_bee_web_scraper_tool import (
    ScrapingBeeWebScraperTool,
)
from language_model_gateway.gateway.tools.sequence_diagram_generator_tool import (
    SequenceDiagramGeneratorTool,
)
from language_model_gateway.gateway.tools.url_to_markdown_tool import URLToMarkdownTool


class ToolProvider:
    def __init__(
        self,
        *,
        image_generator_factory: ImageGeneratorFactory,
        file_manager_factory: FileManagerFactory,
    ) -> None:
        web_search_tool: BaseTool
        default_web_search_tool: str = environ.get(
            "DEFAULT_WEB_SEARCH_TOOL", "duckduckgo"
        )
        match default_web_search_tool:
            case "duckduckgo_search":
                web_search_tool = DuckDuckGoSearchRun()
            case "google_search":
                web_search_tool = GoogleSearchTool()
            case _:
                raise ValueError(
                    f"Unknown default web search tool: {default_web_search_tool}"
                )

        self.tools: Dict[str, BaseTool] = {
            "current_date": CurrentTimeTool(),
            "web_search": web_search_tool,
            "pubmed": PubmedQueryRun(),
            "google_search": GoogleSearchTool(),
            "duckduckgo_search": DuckDuckGoSearchRun(),
            "python_repl": PythonReplTool(),
            "get_web_page": URLToMarkdownTool(),
            "arxiv_search": ArxivQueryRun(),
            "image_generator": ImageGeneratorTool(
                image_generator_factory=image_generator_factory,
                file_manager_factory=file_manager_factory,
                model_provider="aws",
            ),
            "image_generator_openai": ImageGeneratorTool(
                image_generator_factory=image_generator_factory,
                file_manager_factory=file_manager_factory,
                model_provider="openai",
            ),
            "graph_viz_diagram_generator": GraphVizDiagramGeneratorTool(
                file_manager_factory=file_manager_factory
            ),
            "sequence_diagram_generator": SequenceDiagramGeneratorTool(
                file_manager_factory=file_manager_factory
            ),
            "flow_chart_generator": FlowChartGeneratorTool(
                file_manager_factory=file_manager_factory
            ),
            "er_diagram_generator": ERDiagramGeneratorTool(
                file_manager_factory=file_manager_factory
            ),
            "network_topology_generator": NetworkTopologyGeneratorTool(
                file_manager_factory=file_manager_factory
            ),
            "scraping_bee_web_scraper": ScrapingBeeWebScraperTool(
                api_key=environ.get("SCRAPING_BEE_API_KEY")
            ),
            "provider_search": ProviderSearchTool(),
            # "sql_query": QuerySQLDataBaseTool(
            #     db=SQLDatabase(
            #         engine=Engine(
            #             url=environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///:memory:"),
            #             pool=Pool(),
            #             dialect=Dialect()
            #         )
            #     )
            # ),
        }

    def get_tool_by_name(self, *, tool: ToolConfig) -> BaseTool:
        if tool.name in self.tools:
            return self.tools[tool.name]
        raise ValueError(f"Tool with name {tool.name} not found")

    def get_tools(self, *, tools: list[ToolConfig]) -> list[BaseTool]:
        return [self.get_tool_by_name(tool=tool) for tool in tools]
