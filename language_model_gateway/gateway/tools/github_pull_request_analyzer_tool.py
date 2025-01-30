import logging
import os
from datetime import datetime
from typing import Type, Optional, List, Tuple, Literal, Dict

from pydantic import BaseModel, Field

from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool
from language_model_gateway.gateway.utilities.csv_to_markdown_converter import (
    CsvToMarkdownConverter,
)
from language_model_gateway.gateway.utilities.github.github_pull_request import (
    GithubPullRequest,
)
from language_model_gateway.gateway.utilities.github.github_pull_request_helper import (
    GithubPullRequestHelper,
)
from language_model_gateway.gateway.utilities.github.github_pull_request_per_contributor_info import (
    GithubPullRequestPerContributorInfo,
)
from language_model_gateway.gateway.utilities.github.github_pull_request_result import (
    GithubPullRequestResult,
)

logger = logging.getLogger(__name__)


class GitHubPullRequestAnalyzerAgentInput(BaseModel):
    """
    Input model for configuring GitHub Pull Request extraction and analysis.

    IMPORTANT LLM PARSING GUIDANCE:
    - When a query mentions a specific repository, extract the repository name exactly as written
    - When a query includes a GitHub username, extract it as the contributor_name
    - Examples of parsing:
      * "What pull requests from imranq2 in helix.pipelines repo"
        -> repository_name = "helix.pipelines"
        -> contributor_name = "imranq2"
      * "Show pull requests for user johndoe in myorg/myrepo"
        -> repository_name = "myorg/myrepo"
        -> contributor_name = "johndoe"
      * "Pull requests in kubernetes/kubernetes by banzaicloud"
        -> repository_name = "kubernetes/kubernetes"
        -> contributor_name = "banzaicloud"

    Attributes:
        repository_name (Optional[str]):
            Specific repository name to analyze.
            PARSING HINT: Directly use the repository name mentioned in the query.
            Can include organization prefix (e.g., "org/repo").
            Example: "helix.pipelines", "kubernetes/kubernetes"

        contributor_name (Optional[str]):
            GitHub username to filter pull requests.
            PARSING HINT: Extract the GitHub username mentioned in the query.
            Example: "imranq2", "johndoe"

        # ... (rest of the attributes remain the same)
    """

    repository_name: Optional[str] = Field(
        default=None,
        description=(
            "Specific repository name to analyze. "
            "PARSING INSTRUCTION: Extract exact repository name from the query. "
        ),
    )
    contributor_name: Optional[str] = Field(
        default=None,
        description=(
            "GitHub username to filter pull requests. "
            "PARSING INSTRUCTION: Extract GitHub username mentioned in the query."
        ),
    )
    minimum_created_date: Optional[datetime] = Field(
        default=None,
        description="Earliest date for pull request creation (inclusive)",
    )
    maximum_created_date: Optional[datetime] = Field(
        default=None,
        description="Latest date for pull request creation (inclusive)",
    )
    counts_only: Optional[bool] = Field(
        default=False,
        description="Whether to return just count of issues or each issue details",
    )
    sort_by: Optional[Literal["created", "updated", "popularity", "long-running"]] = (
        Field(
            default="created",
            description="Sort pull requests by created, updated, popularity, or long-running.  Default is 'created'.",
        )
    )
    sort_by_direction: Optional[Literal["asc", "desc"]] = Field(
        default="desc",
        description="Sort direction for pull requests.  Choices: 'asc', 'desc'.  Default is 'desc'.",
    )
    use_verbose_logging: Optional[bool] = Field(
        default=False,
        description="Whether to enable verbose logging",
    )
    limit: Optional[int] = Field(
        default=100,
        description="Maximum number of pull requests to retrieve",
    )
    include_description: Optional[bool] = Field(
        default=False,
        description="Whether to include pull request description",
    )


class GitHubPullRequestAnalyzerTool(ResilientBaseTool):
    """
    A LangChain-compatible tool for comprehensive GitHub pull request analysis.

    This tool provides advanced capabilities for extracting and analyzing
    pull request data from a GitHub organization. It supports:
    - Filtering pull requests by repository, date range, and contributor
    - Generating summary reports of pull request activity
    - Retrieving detailed pull request information

    Key Features:
    - Asynchronous pull request retrieval
    - Configurable analysis scope
    - Detailed or summarized reporting
    - Error handling and logging

    Requires:
    - GitHub access token
    - GITHUB_ORGANIZATION_NAME environment variable

    Example Usage:
    ```python
    tool = GitHubPullRequestAnalyzerTool(access_token='your_github_token')
    results, artifact = await tool._arun(
        repository_name='my-project',
        minimum_created_date=datetime(2023, 1, 1),
        include_details=True
    )
    ```
    """

    name: str = "github_pull_request_analyzer"
    description: str = (
        "Advanced GitHub pull request analysis tool. "
        "USAGE TIPS: "
        "- Specify repository with 'in [repo]'. repository can be null for all repos "
        "- Specify contributor with username.  contributor can be null for all contributors "
        "- If querying for a specific date range, include 'from [date] to [date]' "
        "- Set 'counts_only' if you want to get counts only"
        "- Set 'sort_by' to sort by 'created', 'updated', 'popularity', or 'long-running' "
        "- Set 'sort_by_direction' to 'asc' or 'desc' "
        "- Set 'use_verbose_logging' to get verbose logs"
        "- Set 'limit' to limit the number of pull requests to retrieve"
        "- Set 'include_description' to include description"
        "- Example queries: "
        "'Pull requests in kubernetes/kubernetes', "
        "'PRs from johndoe in myorg/myrepo', "
        "'PRs including description from johndoe in myorg/myrepo', "
        "'What pull requests from imranq2 in helix.pipelines repo'"
    )

    args_schema: Type[BaseModel] = GitHubPullRequestAnalyzerAgentInput
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"

    github_pull_request_helper: GithubPullRequestHelper

    # noinspection PyPep8Naming
    def _run(
        self,
        repository_name: Optional[str] = None,
        minimum_created_date: Optional[datetime] = None,
        maximum_created_date: Optional[datetime] = None,
        contributor_name: Optional[str] = None,
        counts_only: Optional[bool] = None,
        sort_by: Optional[
            Literal["created", "updated", "popularity", "long-running"]
        ] = None,
        sort_by_direction: Optional[Literal["asc", "desc"]] = None,
        use_verbose_logging: Optional[bool] = None,
        limit: Optional[int] = None,
        include_description: Optional[bool] = None,
    ) -> Tuple[str, str]:
        """
        Synchronous version of the tool (falls back to async implementation).

        Raises:
            NotImplementedError: Always raises to enforce async usage
        """
        raise NotImplementedError("Use async version of this tool")

    # noinspection PyPep8Naming
    async def _arun(
        self,
        repository_name: Optional[str] = None,
        minimum_created_date: Optional[datetime] = None,
        maximum_created_date: Optional[datetime] = None,
        contributor_name: Optional[str] = None,
        counts_only: Optional[bool] = None,
        sort_by: Optional[
            Literal["created", "updated", "popularity", "long-running"]
        ] = None,
        sort_by_direction: Optional[Literal["asc", "desc"]] = None,
        use_verbose_logging: Optional[bool] = None,
        limit: Optional[int] = None,
        include_description: Optional[bool] = None,
    ) -> Tuple[str, str]:
        """
        Asynchronous version of the GitHub Pull Request extraction tool.

        Returns:
            Tuple of pull request analysis text and artifact description
        """

        log_prefix: str = "GitHubPullRequestAnalyzerAgent: "
        log_prefix_items: List[str] = []
        if repository_name:
            log_prefix_items.append(f"{repository_name=}")
        if minimum_created_date:
            log_prefix_items.append(
                f"minimum_created_date={minimum_created_date.isoformat()}"
            )
        if maximum_created_date:
            log_prefix_items.append(f"maximum_created_date={maximum_created_date}")
        if contributor_name:
            log_prefix_items.append(f"{contributor_name=}")
        if counts_only:
            log_prefix_items.append(f"{counts_only=}")
        if sort_by:
            log_prefix_items.append(f"{sort_by=}")
        if sort_by_direction:
            log_prefix_items.append(f"{sort_by_direction=}")

        log_prefix = log_prefix + ", ".join(log_prefix_items)

        try:
            # Initialize GitHub Pull Request Helper
            # Retrieve closed pull requests
            max_repos: int = int(os.environ.get("GITHUB_MAXIMUM_REPOS", 100))
            max_pull_requests: Optional[int] = (
                int(os.environ.get("GITHUB_MAXIMUM_PULL_REQUESTS_PER_REPO", 100))
                if not counts_only
                else None
            )
            if limit:
                max_pull_requests = limit

            pull_request_result: GithubPullRequestResult = (
                await self.github_pull_request_helper.retrieve_closed_prs(
                    max_repos=max_repos,
                    max_pull_requests=max_pull_requests,
                    min_created_at=minimum_created_date,
                    max_created_at=maximum_created_date,
                    include_merged=True,
                    repo_name=repository_name,
                    sort_by=sort_by,
                    sort_by_direction=sort_by_direction,
                )
            )
            pull_requests: List[GithubPullRequest] = pull_request_result.pull_requests

            full_text: str
            if not counts_only:
                full_text = "Number,Title,User,Created,Closed,Url,State,Description\n"
                for pr in pull_requests:
                    clean_title: str = pr.title.replace('"', "'")
                    clean_body: str = (
                        pr.body.replace('"', "'")
                        if pr.body and include_description
                        else ""
                    )
                    full_text += f'{pr.pull_request_number},"{clean_title}",{pr.user},{pr.created_at},{pr.closed_at},{pr.html_url},{pr.state},"{clean_body}"\n'
            else:
                # Summarize pull requests by engineer
                pr_counts: Dict[str, GithubPullRequestPerContributorInfo] = (
                    self.github_pull_request_helper.summarize_prs_by_engineer(
                        pull_requests=pull_requests
                    )
                )

                full_text = self.github_pull_request_helper.export_results_as_csv(
                    pr_counts=pr_counts
                )

            # Create artifact description
            artifact = log_prefix + f", Analyzed {len(pull_requests)} PRs"
            if pull_request_result.error:
                artifact += f"\nError: {pull_request_result.error}"

            if len(pull_requests) == 0:
                artifact += f"\nQueries:\n{pull_request_result.query}"
            elif use_verbose_logging:
                artifact += f"\nQueries:\n{pull_request_result.query}"
                # artifact += "\n\nRaw:"
                # artifact += f"\n```{full_text}```"

            artifact += "\n\nResults:"
            artifact += f"\n{CsvToMarkdownConverter.csv_to_markdown_table(full_text)}"

            return full_text, artifact

        except Exception as e:
            error_msg = f"Error analyzing GitHub pull requests: {str(e)}"
            error_artifact = log_prefix + " Analysis Failed" + str(e)
            logger.error(error_msg)
            return error_msg, error_artifact
