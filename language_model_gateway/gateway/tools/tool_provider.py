import logging
from typing import Dict, List

from langchain_community.tools import (
    ArxivQueryRun,
)
from langchain_core.tools import BaseTool

from languagemodelcommon.configs.schemas.config_schema import AgentConfig
from languagemodelcommon.file_managers.file_manager_factory import (
    FileManagerFactory,
)
from languagemodelcommon.image_generation.image_generator_factory import (
    ImageGeneratorFactory,
)
from languagemodelcommon.ocr.ocr_extractor_factory import OCRExtractorFactory
from language_model_gateway.gateway.tools.confluence_page_retriever import (
    ConfluencePageRetriever,
)
from language_model_gateway.gateway.tools.confluence_search_tool import (
    ConfluenceSearchTool,
)
from language_model_gateway.gateway.tools.current_time_tool import CurrentTimeTool
from langchain_community.tools.pubmed.tool import PubmedQueryRun

from language_model_gateway.gateway.tools.er_diagram_generator_tool import (
    ERDiagramGeneratorTool,
)
from language_model_gateway.gateway.tools.flow_chart_generator_tool import (
    FlowChartGeneratorTool,
)
from language_model_gateway.gateway.tools.health_summary_generator_tool import (
    HealthSummaryGeneratorTool,
)
from language_model_gateway.gateway.tools.github_pull_request_analyzer_tool import (
    GitHubPullRequestAnalyzerTool,
)
from language_model_gateway.gateway.tools.github_pull_request_diff_tool import (
    GitHubPullRequestDiffTool,
)
from language_model_gateway.gateway.tools.github_pull_request_retriever_tool import (
    GitHubPullRequestRetriever,
)
from language_model_gateway.gateway.tools.graph_viz_diagram_generator_tool import (
    GraphVizDiagramGeneratorTool,
)
from language_model_gateway.gateway.tools.fhir_graphql_schema_provider import (
    GraphqlSchemaProviderTool,
)
from language_model_gateway.gateway.tools.image_generator_tool import ImageGeneratorTool
from language_model_gateway.gateway.tools.jira_issues_analyzer_tool import (
    JiraIssuesAnalyzerTool,
)
from language_model_gateway.gateway.tools.databricks_sql_tool import DatabricksSQLTool

from language_model_gateway.gateway.tools.jira_issue_retriever import (
    JiraIssueRetriever,
)
from language_model_gateway.gateway.tools.user_profile.get_user_profile_tool import (
    GetUserProfileTool,
)
from language_model_gateway.gateway.tools.memories.memory_read_tool import (
    MemoryReadTool,
)
from language_model_gateway.gateway.tools.memories.memory_write_tool import (
    MemoryWriteTool,
)
from language_model_gateway.gateway.tools.user_profile.store_user_profile_tool import (
    StoreUserProfileTool,
)
from language_model_gateway.gateway.tools.network_topology_diagram_tool import (
    NetworkTopologyGeneratorTool,
)
from language_model_gateway.gateway.tools.pdf_extraction_tool import PDFExtractionTool

from language_model_gateway.gateway.tools.person_creator_tool import PersonCreatorTool
from language_model_gateway.gateway.tools.provider_search_tool import ProviderSearchTool
from language_model_gateway.gateway.tools.scraping_bee_web_scraper_tool import (
    ScrapingBeeWebScraperTool,
)
from language_model_gateway.gateway.tools.sequence_diagram_generator_tool import (
    SequenceDiagramGeneratorTool,
)
from language_model_gateway.gateway.tools.calculator_average_tool import (
    CalculatorAverageTool,
)
from language_model_gateway.gateway.tools.calculator_stddev_tool import (
    CalculatorStddevTool,
)
from language_model_gateway.gateway.tools.calculator_sum_tool import CalculatorSumTool
from language_model_gateway.gateway.tools.calculator_length_tool import (
    CalculatorLengthTool,
)
from language_model_gateway.gateway.utilities.confluence.confluence_helper import (
    ConfluenceHelper,
)
from language_model_gateway.gateway.utilities.language_model_gateway_environment_variables import (
    LanguageModelGatewayEnvironmentVariables,
)
from language_model_gateway.gateway.utilities.github.github_pull_request_helper import (
    GithubPullRequestHelper,
)
from language_model_gateway.gateway.utilities.jira.jira_issues_helper import (
    JiraIssueHelper,
)
from language_model_gateway.gateway.utilities.databricks.databricks_helper import (
    DatabricksHelper,
)
from language_model_gateway.gateway.utilities.logger.log_levels import SRC_LOG_LEVELS

logger = logging.getLogger(__name__)
logger.setLevel(SRC_LOG_LEVELS["AGENTS"])


class ToolProvider:
    def __init__(
        self,
        *,
        image_generator_factory: ImageGeneratorFactory,
        file_manager_factory: FileManagerFactory,
        ocr_extractor_factory: OCRExtractorFactory,
        environment_variables: LanguageModelGatewayEnvironmentVariables,
        github_pull_request_helper: GithubPullRequestHelper,
        jira_issues_helper: JiraIssueHelper,
        confluence_helper: ConfluenceHelper,
        databricks_helper: DatabricksHelper,
    ) -> None:
        self.tools: Dict[str, BaseTool] = {
            "current_date": CurrentTimeTool(),
            "calculator_average": CalculatorAverageTool(),
            "calculator_stddev": CalculatorStddevTool(),
            "calculator_sum": CalculatorSumTool(),
            "calculator_length": CalculatorLengthTool(),
            "pubmed": PubmedQueryRun(),
            # "google_search": GoogleSearchTool(),
            # "duckduckgo_search": DuckDuckGoSearchRun(),
            # "python_repl": PythonReplTool(),
            "arxiv_search": ArxivQueryRun(),
            "health_summary_generator": HealthSummaryGeneratorTool(
                file_manager_factory=file_manager_factory,
            ),
            "image_generator": ImageGeneratorTool(
                image_generator_factory=image_generator_factory,
                file_manager_factory=file_manager_factory,
                model_provider="aws",
                environment_variables=environment_variables,
            ),
            "image_generator_openai": ImageGeneratorTool(
                image_generator_factory=image_generator_factory,
                file_manager_factory=file_manager_factory,
                model_provider="openai",
                environment_variables=environment_variables,
            ),
            "graph_viz_diagram_generator": GraphVizDiagramGeneratorTool(
                file_manager_factory=file_manager_factory,
                environment_variables=environment_variables,
            ),
            "sequence_diagram_generator": SequenceDiagramGeneratorTool(
                file_manager_factory=file_manager_factory,
                environment_variables=environment_variables,
            ),
            "flow_chart_generator": FlowChartGeneratorTool(
                file_manager_factory=file_manager_factory,
                environment_variables=environment_variables,
            ),
            "er_diagram_generator": ERDiagramGeneratorTool(
                file_manager_factory=file_manager_factory,
                environment_variables=environment_variables,
            ),
            "network_topology_generator": NetworkTopologyGeneratorTool(
                file_manager_factory=file_manager_factory,
                environment_variables=environment_variables,
            ),
            "scraping_bee_web_scraper": ScrapingBeeWebScraperTool(
                api_key=environment_variables.scraping_bee_api_key,
                environment_variables=environment_variables,
            ),
            "provider_search": ProviderSearchTool(
                environment_variables=environment_variables,
            ),
            "pdf_text_extractor": PDFExtractionTool(
                ocr_extractor_factory=ocr_extractor_factory
            ),
            "github_pull_request_analyzer": GitHubPullRequestAnalyzerTool(
                github_pull_request_helper=github_pull_request_helper,
                environment_variables=environment_variables,
            ),
            "github_pull_request_diff": GitHubPullRequestDiffTool(
                github_pull_request_helper=github_pull_request_helper
            ),
            "jira_issues_analyzer": JiraIssuesAnalyzerTool(
                jira_issues_helper=jira_issues_helper,
                environment_variables=environment_variables,
            ),
            "databricks_query_validator": DatabricksSQLTool(
                databricks_helper=databricks_helper
            ),
            "person_creator": PersonCreatorTool(),
            "fhir_graphql_schema_provider": GraphqlSchemaProviderTool(),
            "jira_issue_retriever": JiraIssueRetriever(
                jira_issues_helper=jira_issues_helper
            ),
            "github_pull_request_retriever": GitHubPullRequestRetriever(
                github_pull_request_helper=github_pull_request_helper
            ),
            "confluence_search_tool": ConfluenceSearchTool(
                confluence_helper=confluence_helper
            ),
            "confluence_page_retriever": ConfluencePageRetriever(
                confluence_helper=confluence_helper
            ),
            "get_user_profile": GetUserProfileTool(),
            "store_user_profile": StoreUserProfileTool(),
            "memory_writer": MemoryWriteTool(),
            "memory_reader": MemoryReadTool(),
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

    def get_tool_by_name(
        self, *, tool: AgentConfig, headers: Dict[str, str]
    ) -> BaseTool:
        tool_names: List[str] = [name for name in self.tools.keys()]
        if tool.name in tool_names:
            return self.tools[tool.name]
        raise ValueError(
            f"Tool with name {tool.name} not found in available tools: {','.join(tool_names)}"
        )

    def has_tool(self, *, tool: AgentConfig) -> bool:
        tool_names: List[str] = [name for name in self.tools.keys()]
        return tool.name in tool_names

    def get_tools(
        self, *, tools: list[AgentConfig], headers: Dict[str, str]
    ) -> list[BaseTool]:
        return [
            self.get_tool_by_name(tool=tool, headers=headers)
            for tool in tools
            if self.has_tool(tool=tool)
        ]
