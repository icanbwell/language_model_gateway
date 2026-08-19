import base64
import logging
from datetime import datetime
from logging import Logger
from typing import Dict, Optional, List, Any, Literal

from httpx import URL

from languagemodelcommon.http.http_client_factory import HttpClientFactory
from language_model_gateway.gateway.utilities.jira.JiraIssuesPerAssigneeInfo import (
    JiraIssuesPerAssigneeInfo,
)
from language_model_gateway.gateway.utilities.jira.jira_issue import JiraIssue
from language_model_gateway.gateway.utilities.jira.jira_issue_result import (
    JiraIssueResult,
)


class JiraIssueHelper:
    def __init__(
        self,
        *,
        http_client_factory: HttpClientFactory,
        jira_base_url: Optional[str],
        access_token: Optional[str],
        username: Optional[str],
    ):
        """
        Initialize Jira Issue Helper with async rate limit handling.

        Args:
            jira_base_url (str): Base URL of the Jira instance
            access_token (str): Jira API token or personal access token
        """
        self.http_client_factory: HttpClientFactory = http_client_factory
        self.logger: Logger = logging.getLogger(__name__)
        self.jira_base_url: Optional[str] = (
            jira_base_url.rstrip("/") if jira_base_url else None
        )
        self.jira_access_token: Optional[str] = access_token
        self.username: Optional[str] = username

        credentials = base64.b64encode(f"{username}:{access_token}".encode()).decode()

        self.headers = {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "AsyncJiraIssueHelper",
        }

    async def retrieve_closed_issues(
        self,
        *,
        max_projects: Optional[int] = None,
        max_issues: Optional[int] = None,
        min_created_at: Optional[datetime] = None,
        max_created_at: Optional[datetime] = None,
        min_updated_at: Optional[datetime] = None,
        max_updated_at: Optional[datetime] = None,
        project_key: Optional[str] = None,
        assignee: Optional[str] = None,
        sort_by: Optional[Literal["updated", "created", "resolved"]] = None,
        sort_by_direction: Optional[Literal["asc", "desc"]] = None,
        include_full_description: Optional[bool] = False,
        status: Optional[str] = "Closed",
    ) -> JiraIssueResult:
        """
        Async method to retrieve closed issues across Jira projects.

        Args:
            max_projects (int, optional): Maximum number of projects to fetch
            max_issues (int, optional): Maximum number of issues to retrieve
            min_created_at (datetime, optional): Minimum creation date
            max_created_at (datetime, optional): Maximum creation date
            min_updated_at (datetime, optional): Minimum updated date
            max_updated_at (datetime, optional): Maximum updated date
            project_key (str, optional): Specific project to fetch issues from
            assignee (str, optional): Specific assignee to filter issues
            sort_by (str, optional): Field to sort by
            sort_by_direction (str, optional): Sort direction
            include_full_description (bool, optional): Include full description
            status: (str, Optional): match status

        Returns:
            List[JiraIssue]: List of closed Jira issues
        """
        if not self.jira_base_url:
            raise ValueError("Jira base URL is required")
        if not self.jira_access_token:
            raise ValueError("Jira access token is required")

        async with self.http_client_factory.create_http_client(
            base_url=self.jira_base_url, headers=self.headers, timeout=30.0
        ) as client:
            query: str = ""
            try:
                # Construct JQL (Jira Query Language) based on parameters
                jql_conditions = [f"status = '{status}'"]

                if project_key:
                    jql_conditions.append(f"project = '{project_key}'")

                if min_created_at:
                    jql_conditions.append(
                        f"created >= '{min_created_at.strftime('%Y-%m-%d')}'"
                    )

                if max_created_at:
                    jql_conditions.append(
                        f"created <= '{max_created_at.strftime('%Y-%m-%d')}'"
                    )

                if min_updated_at:
                    jql_conditions.append(
                        f"updated >= '{min_updated_at.strftime('%Y-%m-%d')}'"
                    )

                if max_updated_at:
                    jql_conditions.append(
                        f"updated <= '{max_updated_at.strftime('%Y-%m-%d')}'"
                    )

                if assignee:
                    jql_conditions.append(f"assignee = '{assignee}'")

                jql = " AND ".join(jql_conditions)

                # order the list descending by updated date
                if sort_by:
                    if not sort_by_direction:
                        sort_by_direction = "desc"
                    jql += f" ORDER BY {sort_by} {sort_by_direction}"
                else:
                    jql += " ORDER BY updated desc"

                # Pagination parameters
                max_results = max_issues or 100  # * (max_projects or 10)

                closed_issues_list: List[JiraIssue] = []
                pages_remaining = True
                next_page_token: Optional[str] = None

                while pages_remaining:
                    # https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-jql-post
                    params = {
                        "jql": jql,
                        # "startAt": start_at,
                        "nextPageToken": next_page_token,
                        "maxResults": max_results,
                        "fields": [
                            # "*all",
                            "id",
                            "summary",
                            "status",
                            "created",
                            "resolutiondate",
                            "assignee",
                            "assignee",
                            "reporter",
                            "creator",
                            "project",
                            "issuetype",
                            "priority",
                            "description",
                        ],
                    }
                    response = await client.post(
                        f"{self.jira_base_url}/rest/api/3/search/jql",
                        json=params,
                    )
                    response.raise_for_status()

                    url: URL = response.request.url
                    query += f"{url}: {response.request.content.decode()}\n"

                    issues_data = response.json()

                    for issue in issues_data.get("issues", []):
                        fields_ = issue["fields"]
                        assignee_object: Optional[Dict[str, Any]] = fields_.get(
                            "assignee", {}
                        )
                        assignee_name: str = (
                            assignee_object.get("displayName", "Unassigned")
                            if assignee_object
                            else "Unassigned"
                        )
                        assignee_email: str = (
                            assignee_object.get("emailAddress", "Unassigned")
                            if assignee_object
                            else "Unassigned"
                        )
                        reporter_object: Optional[Dict[str, Any]] = fields_.get(
                            "reporter", {}
                        )
                        reporter_name: str = (
                            reporter_object.get("displayName", "Unassigned")
                            if reporter_object
                            else "Unassigned"
                        )
                        reporter_email: str = (
                            reporter_object.get("emailAddress", "Unassigned")
                            if reporter_object
                            else "Unassigned"
                        )
                        creator_object: Optional[Dict[str, Any]] = fields_.get(
                            "creator", {}
                        )
                        creator_name: str = (
                            creator_object.get("displayName", "Unassigned")
                            if creator_object
                            else "Unassigned"
                        )
                        creator_email: str = (
                            creator_object.get("emailAddress", "Unassigned")
                            if creator_object
                            else "Unassigned"
                        )
                        issue_type: str = fields_.get("issuetype", {}).get("name")
                        project_name: str = fields_.get("project", {}).get("name")

                        def read_description(description: Dict[str, Any] | None) -> str:
                            if not include_full_description:
                                return ""
                            if not description:
                                return ""
                            try:
                                description1 = ""
                                content: List[Dict[str, Any]] = description.get(
                                    "content", []
                                )
                                for item in content:
                                    if item.get("type") == "paragraph":
                                        for element in item.get("content", []):
                                            if element.get("type") == "text":
                                                description1 += element.get("text", "")
                                return description1
                            except Exception as e:
                                self.logger.error(
                                    f"Error reading description: {e}: {description}"
                                )
                                return ""

                        item_description: str = read_description(
                            fields_.get("description", {})
                        )
                        issue_priority: str = fields_.get("priority", {}).get("name")
                        closed_issues_list.append(
                            JiraIssue(
                                key=issue.get("key"),
                                url=issue.get("self"),
                                summary=fields_.get("summary", "No Summary"),
                                status=fields_.get("status", {}).get("name"),
                                created_at=datetime.fromisoformat(
                                    fields_["created"].replace("Z", "+00:00")
                                ),
                                closed_at=(
                                    datetime.fromisoformat(
                                        fields_.get("resolutiondate", "").replace(
                                            "Z", "+00:00"
                                        )
                                    )
                                    if fields_.get("resolutiondate")
                                    else None
                                ),
                                assignee=assignee_name,
                                assignee_email=assignee_email,
                                reporter=reporter_name,
                                reporter_email=reporter_email,
                                creator=creator_name,
                                creator_email=creator_email,
                                issue_type=issue_type,
                                project_name=project_name,
                                description=item_description,
                                priority=issue_priority,
                                project=fields_.get("project", {}).get("key"),
                            )
                        )

                        if max_issues and len(closed_issues_list) >= max_issues:
                            break

                    # Break if no more issues or max issues reached
                    if (not issues_data.get("issues")) or (
                        max_issues and len(closed_issues_list) >= max_issues
                    ):
                        pages_remaining = False

                    next_page_token = issues_data.get("nextPageToken")
                    if next_page_token is None:
                        pages_remaining = False

                return JiraIssueResult(
                    issues=closed_issues_list, query=query, error=None
                )

            except Exception as e:
                return JiraIssueResult(
                    issues=[],
                    query=query,
                    error=str(e),
                )

    # noinspection PyMethodMayBeStatic
    def summarize_issues_by_assignee(
        self, *, issues: List[JiraIssue]
    ) -> Dict[str, JiraIssuesPerAssigneeInfo]:
        """
        Summarize issues by assignee.

        Args:
            issues (List[JiraIssue]): List of Jira issues

        Returns:
            Dict[str, Dict[str, Any]]: Summary of issues by assignee
        """
        assignee_issue_counts: Dict[str, JiraIssuesPerAssigneeInfo] = {}

        for issue in issues:
            assignee = issue.assignee or "Unassigned"

            if assignee not in assignee_issue_counts:
                assignee_issue_counts[assignee] = JiraIssuesPerAssigneeInfo(
                    assignee=assignee,
                    issue_count=1,
                    projects=[issue.project] if issue.project else [],
                )
            else:
                assignee_issue_counts[assignee].issue_count += 1
                projects = assignee_issue_counts[assignee].projects
                if projects is not None:
                    if issue.project is not None and issue.project not in projects:
                        projects.append(issue.project)

        # Sort by issue count
        return dict(
            sorted(
                assignee_issue_counts.items(),
                key=lambda item: item[1].issue_count,
                reverse=True,
            )
        )

    def export_results(
        self,
        *,
        issue_counts: Dict[str, JiraIssuesPerAssigneeInfo],
        output_file: str,
    ) -> None:
        """
        Export issue count results to console and optional file.

        Args:
            issue_counts (Dict[str, Dict[str, Any]]): Issue counts by assignee
            output_file (Optional[str]): Path to output file
        """
        if not issue_counts:
            raise ValueError("Issue counts are required")
        if not output_file:
            raise ValueError("Output file path is invalid")

        try:
            # Security note (Aikido path-traversal finding, BAI-441): `output_file` is not
            # currently reachable from any request/LLM-tool input — this method is only
            # invoked from tests with a hardcoded path, and it is not wired into any
            # LangChain tool's args_schema exposed to the model. If a caller ever passes
            # this a value derived from a request, config file, or LLM tool call, add
            # path-containment validation (resolve to an absolute path and confirm it
            # stays inside an expected base directory) before opening it for write.
            with open(output_file, "w") as f:
                f.write(self.export_results_to_csv(issue_counts=issue_counts))
            self.logger.info(f"Results exported to {output_file}")
        except IOError as e:
            self.logger.error(f"Failed to export results: {e}")

    # noinspection PyMethodMayBeStatic
    def export_results_to_csv(
        self,
        *,
        issue_counts: Dict[str, JiraIssuesPerAssigneeInfo],
    ) -> str:
        """
        Export issue count results to console and optional file.

        Args:
            issue_counts (Dict[str, Dict[str, Any]]): Issue counts by assignee
        """

        result: str = "Assignee,IssueCount,Projects\n"
        for assignee, info in issue_counts.items():
            projects_text: str = " | ".join(info.projects) if info.projects else ""
            result += f'{assignee},{info.issue_count},"{projects_text}"\n'
        return result

    async def retrieve_issue_by_id(
        self,
        issue_id: str,
    ) -> JiraIssueResult:
        """
        Async method to retrieve a specific Jira issue by ID.

        Args:
            issue_id (str): The ID of the Jira issue to retrieve

        Returns:
            JiraIssueResult: The result containing the Jira issue
        """
        if not self.jira_base_url:
            raise ValueError("Jira base URL is required")
        if not self.jira_access_token:
            raise ValueError("Jira access token is required")

        async with self.http_client_factory.create_http_client(
            base_url=self.jira_base_url, headers=self.headers, timeout=30.0
        ) as client:
            query: str = ""
            try:
                response = await client.get(
                    f"{self.jira_base_url}/rest/api/3/issue/{issue_id}"
                )
                response.raise_for_status()

                url: URL = response.request.url
                query += f"{url}: {response.request.content.decode()}\n"

                issue_data = response.json()
                fields_ = issue_data["fields"]

                assignee_object: Optional[Dict[str, Any]] = fields_.get("assignee", {})
                assignee_name: str = (
                    assignee_object.get("displayName", "Unassigned")
                    if assignee_object
                    else "Unassigned"
                )
                assignee_email: str = (
                    assignee_object.get("emailAddress", "Unassigned")
                    if assignee_object
                    else "Unassigned"
                )
                reporter_object: Optional[Dict[str, Any]] = fields_.get("reporter", {})
                reporter_name: str = (
                    reporter_object.get("displayName", "Unassigned")
                    if reporter_object
                    else "Unassigned"
                )
                reporter_email: str = (
                    reporter_object.get("emailAddress", "Unassigned")
                    if reporter_object
                    else "Unassigned"
                )
                creator_object: Optional[Dict[str, Any]] = fields_.get("creator", {})
                creator_name: str = (
                    creator_object.get("displayName", "Unassigned")
                    if creator_object
                    else "Unassigned"
                )
                creator_email: str = (
                    creator_object.get("emailAddress", "Unassigned")
                    if creator_object
                    else "Unassigned"
                )
                issue_type: str = fields_.get("issuetype", {}).get("name")
                project_name: str = fields_.get("project", {}).get("name")

                def read_description(description: Dict[str, Any] | None) -> str:
                    if not description:
                        return ""
                    try:
                        description1 = ""
                        content: List[Dict[str, Any]] = description.get("content", [])
                        for item in content:
                            if item.get("type") == "paragraph":
                                for element in item.get("content", []):
                                    if element.get("type") == "text":
                                        description1 += element.get("text", "")
                        return description1
                    except Exception as e:
                        self.logger.error(
                            f"Error reading description: {e}: {description}"
                        )
                        return ""

                item_description: str = read_description(fields_.get("description", {}))
                issue_priority: str = fields_.get("priority", {}).get("name")

                jira_issue = JiraIssue(
                    key=issue_data.get("key"),
                    url=issue_data.get("self"),
                    summary=fields_.get("summary", "No Summary"),
                    status=fields_.get("status", {}).get("name"),
                    created_at=datetime.fromisoformat(
                        fields_["created"].replace("Z", "+00:00")
                    ),
                    closed_at=(
                        datetime.fromisoformat(
                            fields_.get("resolutiondate", "").replace("Z", "+00:00")
                        )
                        if fields_.get("resolutiondate")
                        else None
                    ),
                    assignee=assignee_name,
                    assignee_email=assignee_email,
                    reporter=reporter_name,
                    reporter_email=reporter_email,
                    creator=creator_name,
                    creator_email=creator_email,
                    issue_type=issue_type,
                    project_name=project_name,
                    description=item_description,
                    priority=issue_priority,
                    project=fields_.get("project", {}).get("key"),
                )

                return JiraIssueResult(issues=[jira_issue], query=query, error=None)

            except Exception as e:
                return JiraIssueResult(issues=[], query=query, error=str(e))
