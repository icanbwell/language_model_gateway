import logging
import os
from datetime import datetime
from typing import Type, Optional, List, Tuple, Literal, Annotated

from langgraph.prebuilt import InjectedState
from pydantic import BaseModel, Field

from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool
from language_model_gateway.gateway.utilities.csv_to_markdown_converter import (
    CsvToMarkdownConverter,
)
from language_model_gateway.gateway.utilities.jira.jira_issue import JiraIssue
from language_model_gateway.gateway.utilities.jira.jira_issue_result import (
    JiraIssueResult,
)
from language_model_gateway.gateway.utilities.jira.jira_issues_helper import (
    JiraIssueHelper,
)

logger = logging.getLogger(__name__)


class JiraIssuesAnalyzerAgentInput(BaseModel):
    """
    Input model for configuring Jira data extraction and analysis.
    """

    project_name: Optional[str] = Field(
        default=None,
        description=(
            "Optional specific project name to analyze. "
            "PARSING INSTRUCTION: Extract exact project name from the query if query specifies a project name. "
        ),
    )
    assignee: Optional[str] = Field(
        default=None,
        description=(
            "Optional Jira username to filter issues. "
            "PARSING INSTRUCTION: Extract Jira username mentioned in the query."
        ),
    )
    minimum_created_date: Optional[datetime] = Field(
        default=None,
        description="Earliest date for issue creation (inclusive)",
    )
    maximum_created_date: Optional[datetime] = Field(
        default=None,
        description="Latest date for issue creation (inclusive)",
    )
    minimum_updated_date: Optional[datetime] = Field(
        default=None,
        description="Earliest date for issue update (inclusive)",
    )
    maximum_updated_date: Optional[datetime] = Field(
        default=None,
        description="Latest date for issue update (inclusive)",
    )
    counts_only: Optional[bool] = Field(
        default=False,
        description="Whether to return just count of issues or each issue details",
    )
    sort_by: Optional[Literal["updated", "created", "resolved"]] = Field(
        default="updated",
        description="Field to sort by.  Choices: 'updated', 'created', 'resolved'.  Default is 'updated'.",
    )
    sort_by_direction: Optional[Literal["asc", "desc"]] = Field(
        default="desc",
        description="Sort direction for jira issues. Choices: 'asc', 'desc'.  Default is 'desc'.",
    )
    include_full_description: Optional[bool] = Field(
        default=False,
        description="Include full issue description or just summary",
    )
    use_verbose_logging: Optional[bool] = Field(
        default=False,
        description="Whether to enable verbose logging",
    )
    limit: Optional[int] = Field(
        default=100,
        description="Maximum number of jira issues to retrieve",
    )
    auth_token: Annotated[Optional[str], InjectedState("auth_token")] = Field(
        default=None,
        description="Injected state",
    )


class JiraIssuesAnalyzerTool(ResilientBaseTool):
    """
    A LangChain-compatible tool for comprehensive Jira issue analysis.

    This tool can be used to extract and analyze Jira issues across projects and assignees.

    """

    name: str = "jira_issues_analyzer"
    description: str = (
        "Advanced Jira Issue analysis tool. "
        "USAGE TIPS: "
        "- Specify assignee with username "
        "- If querying for a specific date range, include 'from [date] to [date]' "
        "- Set 'counts_only' if you want to get counts only"
        "- Set include_full_description to get full issue description"
        "- Set 'sort_by' to sort by 'created', 'updated', 'popularity', or 'long-running' "
        "- Set 'sort_by_direction' to 'asc' or 'desc' "
        "- Set 'use_verbose_logging' to get verbose logs"
        "- Set 'limit' to get a specific number of issues"
        "- Example queries: "
        "'Pull issues in EFS', "
        "'Issues assigned to johndoe in EFS', "
        "'What issues assigned to imranq2 in EFS project'"
        "'Get last 10 issues'"
    )

    args_schema: Type[BaseModel] = JiraIssuesAnalyzerAgentInput
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"

    jira_issues_helper: JiraIssueHelper

    # noinspection PyPep8Naming
    def _run(
        self,
        project_name: Optional[str] = None,
        minimum_created_date: Optional[datetime] = None,
        maximum_created_date: Optional[datetime] = None,
        minimum_updated_date: Optional[datetime] = None,
        maximum_updated_date: Optional[datetime] = None,
        assignee: Optional[str] = None,
        counts_only: Optional[bool] = None,
        sort_by: Optional[Literal["updated", "created", "resolved"]] = None,
        sort_by_direction: Optional[Literal["asc", "desc"]] = None,
        include_full_description: Optional[bool] = None,
        use_verbose_logging: Optional[bool] = None,
        limit: Optional[int] = None,
        auth_token: Optional[str] = None,
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
        project_name: Optional[str] = None,
        minimum_created_date: Optional[datetime] = None,
        maximum_created_date: Optional[datetime] = None,
        minimum_updated_date: Optional[datetime] = None,
        maximum_updated_date: Optional[datetime] = None,
        assignee: Optional[str] = None,
        counts_only: Optional[bool] = None,
        sort_by: Optional[Literal["updated", "created", "resolved"]] = None,
        sort_by_direction: Optional[Literal["asc", "desc"]] = None,
        include_full_description: Optional[bool] = None,
        use_verbose_logging: Optional[bool] = None,
        limit: Optional[int] = None,
        auth_token: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Asynchronous version of the Jira Issues analyzer tool.

        Returns:
            Tuple of Jira issue text and artifact description
        """

        log_prefix: str = "JiraIssuesAnalyzerAgent: "
        log_prefix_items: List[str] = []
        if project_name:
            log_prefix_items.append(f"{project_name=}")
        if minimum_created_date:
            log_prefix_items.append(
                f"minimum_created_date={minimum_created_date.isoformat()}"
            )
        if maximum_created_date:
            log_prefix_items.append(
                f"maximum_created_date={maximum_created_date.isoformat()}"
            )
        if minimum_updated_date:
            log_prefix_items.append(
                f"minimum_updated_date={minimum_updated_date.isoformat()}"
            )
        if maximum_updated_date:
            log_prefix_items.append(
                f"maximum_updated_date={maximum_updated_date.isoformat()}"
            )
        if assignee:
            log_prefix_items.append(f"{assignee=}")
        if counts_only:
            log_prefix_items.append(f"{counts_only=}")
        if sort_by:
            log_prefix_items.append(f"{sort_by=}")

        log_prefix += ", ".join(log_prefix_items)

        try:
            max_projects: int = int(os.environ.get("JIRA_MAXIMUM_PROJECTS", 100))
            max_issues: int = int(
                os.environ.get("JIRA_MAXIMUM_ISSUES_PER_PROJECT", 100)
            )
            if limit:
                max_issues = limit
            jira_issues_result: JiraIssueResult = (
                await self.jira_issues_helper.retrieve_closed_issues(
                    max_projects=max_projects,
                    max_issues=max_issues,
                    min_created_at=minimum_created_date,
                    max_created_at=maximum_created_date,
                    min_updated_at=minimum_updated_date,
                    max_updated_at=maximum_updated_date,
                    project_key=project_name,
                    assignee=assignee,
                    sort_by=sort_by,
                    sort_by_direction=sort_by_direction,
                    include_full_description=include_full_description,
                )
            )

            if jira_issues_result.error:
                error_msg = f"Error analyzing Jira issues: {jira_issues_result.error}"
                error_artifact = (
                    log_prefix + f" Analysis Failed: {jira_issues_result.error}"
                )
                logger.error(error_msg)
                return error_msg, error_artifact

            jira_issues: List[JiraIssue] = jira_issues_result.issues

            full_text: str
            if not counts_only:
                full_text = "Id,Summary,Status,Assignee,Created,Closed\n"
                for issue in jira_issues:
                    clean_summary: str = issue.summary.replace('"', "'")
                    full_text += f'{issue.key},"{clean_summary}",{issue.status},{issue.assignee},{issue.created_at.date().isoformat()},{issue.closed_at.date().isoformat() if issue.closed_at else "N/A"}\n'
            else:
                # Summarize issues by engineer
                pr_summary = self.jira_issues_helper.summarize_issues_by_assignee(
                    issues=jira_issues
                )
                full_text = self.jira_issues_helper.export_results_to_csv(
                    issue_counts=pr_summary
                )

            # Create artifact description
            artifact = log_prefix + f", Analyzed {len(jira_issues)} closed issues."
            if jira_issues_result.error:
                artifact += f"\nError: {jira_issues_result.error}"
            if len(jira_issues) == 0:
                artifact += f"\nJira Query:\n{jira_issues_result.query}"
            elif use_verbose_logging:
                artifact += f"\nJira Query: {jira_issues_result.query}"

            artifact += "\n\nResults:"
            artifact += f"\n{CsvToMarkdownConverter.csv_to_markdown_table(full_text)}"

            return full_text, artifact

        except Exception as e:
            error_msg = f"Error analyzing Jira issues: {str(e)}"
            error_artifact = log_prefix + " Analysis Failed: " + str(e)
            logger.error(error_msg)
            return error_msg, error_artifact
