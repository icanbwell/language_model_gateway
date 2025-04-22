import logging

from pydantic import BaseModel, Field

from typing import Type, Optional, Tuple, Literal
from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool
from language_model_gateway.gateway.utilities.github.github_pull_request import (
    GithubPullRequest,
)
from language_model_gateway.gateway.utilities.github.github_pull_request_helper import (
    GithubPullRequestHelper,
)

logger = logging.getLogger(__name__)


class GitHubPullRequestRetrieverInput(BaseModel):
    """Input model for GitHub Pull Request retriever tool."""

    url: str = Field(
        ...,
        title="Pull Request URL",
        description="URL of the GitHub pull request to retrieve information from",
    )
    use_verbose_logging: Optional[bool] = Field(
        default=False,
        description="Whether to enable verbose logging",
    )


class GitHubPullRequestRetriever(ResilientBaseTool):
    """
    LangChain-compatible tool for retrieving information about a GitHub pull request.
    """

    name: str = "github_pull_request_retriever"
    description: str = "Retrieves information about a GitHub pull request given its URL, such as title, description, etc."

    args_schema: Type[BaseModel] = GitHubPullRequestRetrieverInput
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"

    github_pull_request_helper: GithubPullRequestHelper

    def _run(
        self,
        url: Optional[str] = None,
        use_verbose_logging: Optional[bool] = None,
    ) -> Tuple[str, str]:
        """
        Synchronous version of the tool (falls back to async implementation).

        Raises:
            NotImplementedError: Always raises to enforce async usage
        """
        raise NotImplementedError("Use async version of this tool")

    async def _arun(
        self,
        url: Optional[str] = None,
        use_verbose_logging: Optional[bool] = None,
    ) -> Tuple[str, str]:
        """
        Asynchronous version of the GitHub Pull Request retriever tool.

        Returns:
            Tuple of pull request information and artifact description
        """
        assert url, "Pull request URL is required"

        try:
            pull_request: GithubPullRequest = (
                await self.github_pull_request_helper.get_pr_info(pr_url=url)
            )
            artifact = f"GitHubPullRequestRetriever: Retrieved information for {url}"
            if use_verbose_logging:
                artifact += f"\n===== Pull Request Info =====\n{pull_request}\n===== End of Info ====="
            return str(pull_request), artifact

        except Exception as e:
            error_msg = f"Error retrieving GitHub pull request: {str(e)}"
            error_artifact = "GitHubPullRequestRetriever: Retrieval failed"
            logger.error(error_msg)
            return error_msg, error_artifact
