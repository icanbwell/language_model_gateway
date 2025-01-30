import asyncio
import logging
import os
import re
from datetime import datetime
from logging import Logger
from typing import Dict, Optional, List, Union, Any, Literal
from urllib.parse import urlparse

import httpx
from httpx import Response, URL

from language_model_gateway.gateway.http.http_client_factory import HttpClientFactory
from language_model_gateway.gateway.utilities.github.github_pull_request import (
    GithubPullRequest,
)
from language_model_gateway.gateway.utilities.github.github_pull_request_per_contributor_info import (
    GithubPullRequestPerContributorInfo,
)
from language_model_gateway.gateway.utilities.github.github_pull_request_result import (
    GithubPullRequestResult,
)


class GithubPullRequestHelper:
    def __init__(
        self,
        *,
        http_client_factory: HttpClientFactory,
        org_name: Optional[str],
        access_token: Optional[str],
    ):
        """
        Initialize GitHub PR Counter with async rate limit handling.

        Args:
            org_name (str): GitHub organization name
            access_token (str): GitHub Personal Access Token
        """

        self.http_client_factory: HttpClientFactory = http_client_factory
        self.logger: Logger = logging.getLogger(__name__)
        self.org_name: Optional[str] = org_name
        self.github_access_token: Optional[str] = access_token

        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AsyncGithubPullRequestHelper",
        }

    async def _get_rate_limit_info(self, client: httpx.AsyncClient) -> Dict[str, int]:
        """
        Retrieve and log GitHub API rate limit information.

        Returns:
            Dict[str, int]: Rate limit details
        """
        try:
            response = await client.get(
                f"{self.base_url}/rate_limit", headers=self.headers
            )
            response.raise_for_status()
            rate_limit_data = response.json()
            core_rate_limit = rate_limit_data["resources"]["core"]

            return {
                "remaining": core_rate_limit["remaining"],
                "reset_time": core_rate_limit["reset"],
            }
        except Exception as e:
            self.logger.error(f"Rate limit fetch error: {e}")
            raise

    async def _wait_for_rate_limit_reset(self, reset_time: int) -> None:
        """
        Async wait until rate limit resets.

        Args:
            reset_time (int): Timestamp when rate limit will reset
        """
        current_time = int(asyncio.get_event_loop().time())
        wait_time = max(reset_time - current_time + 5, 0)
        if wait_time > 0:
            self.logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds.")
            await asyncio.sleep(wait_time)

    async def retrieve_closed_prs(
        self,
        *,
        max_repos: Optional[int] = None,
        max_pull_requests: Optional[int] = None,
        min_created_at: Optional[datetime] = None,
        max_created_at: Optional[datetime] = None,
        include_merged: bool = True,
        repo_name: Optional[str] = None,
        sort_by: Optional[
            Literal["created", "updated", "popularity", "long-running"]
        ] = None,
        sort_by_direction: Optional[Literal["asc", "desc"]] = None,
        status: Optional[Literal["closed"]] = None,
    ) -> GithubPullRequestResult:
        """
        Async method to retrieve closed pull requests across organization repositories.
        """

        assert self.org_name, "Organization name is required"
        assert self.github_access_token, "GitHub access token is required"

        if os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1":
            self.logger.info(
                f"Retrieving closed PRs for {self.org_name} organization"
                f" with max_repos={max_repos}, max_pull_requests={max_pull_requests},"
                f" min_created_at={min_created_at}, max_created_at={max_created_at},"
                f" include_merged={include_merged}, repo_name={repo_name},"
                f" sort_by={sort_by}, sort_by_direction={sort_by_direction},"
                f" status={status}"
            )

        async with self.http_client_factory.create_http_client(
            base_url=self.base_url, headers=self.headers, timeout=30.0
        ) as client:
            query: str = ""
            try:
                if repo_name:
                    repos_url = f"{self.base_url}/repos/{self.org_name}/{repo_name}"
                    if os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1":
                        self.logger.info(f"Fetching repository: {repos_url}")
                    repo_response = await client.get(
                        repos_url,
                        headers={
                            "Accept": "application/vnd.github+json",
                            **self.headers,
                        },
                    )

                    if not query:
                        url: URL = repo_response.request.url
                        query += f"\n{str(url)}"
                    repo_response.raise_for_status()
                    repos = [repo_response.json()]
                else:
                    # Fetch organization repositories
                    repos_url = f"{self.base_url}/orgs/{self.org_name}/repos"
                    pages_remaining = True
                    repos = []

                    page_number: int = 1
                    while pages_remaining:
                        params: Dict[str, Any] = {
                            "type": "all",
                            "sort": "pushed",
                            "direction": "desc",
                            "per_page": max_repos or 50,
                            "page": page_number,
                        }
                        if os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1":
                            self.logger.info(
                                f"Fetching repositories: {repos_url}: {params}"
                            )
                        repos_response = await client.get(
                            repos_url,
                            headers={
                                "Accept": "application/vnd.github+json",
                                **self.headers,
                            },
                            params=params,
                        )
                        url = repos_response.request.url
                        query += f"\n{str(url)}"

                        repos_response.raise_for_status()
                        repos.extend(repos_response.json())
                        if max_repos and len(repos) >= max_repos:
                            pages_remaining = False
                        elif len(repos_response.json()) == 0:
                            pages_remaining = False
                        page_number += 1

                # Limit repositories if max_repos is specified
                repos = repos[:max_repos] if max_repos else repos

                closed_prs_list: List[GithubPullRequest] = []

                for repo in repos:
                    # Fetch closed PRs for the repository
                    prs_url = (
                        f"{self.base_url}/repos/{self.org_name}/{repo['name']}/pulls"
                    )
                    pages_remaining = True
                    prs: List[Dict[str, Any]] = []
                    page_number = 1

                    while pages_remaining:
                        params = {
                            "state": status or "closed",
                            "sort": sort_by or "created",
                            "direction": sort_by_direction or "desc",
                            "per_page": max_pull_requests or 50,
                            "page": page_number,
                        }
                        if os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1":
                            self.logger.info(f"Fetching PRs: {prs_url}: {params}")

                        prs_response = await client.get(
                            prs_url,
                            params=params,
                        )
                        query += f"\n{str(prs_response.request.url)}"
                        prs_response.raise_for_status()
                        prs.extend(prs_response.json())
                        if len(prs_response.json()) == 0:
                            pages_remaining = False
                        else:
                            if max_pull_requests and len(prs) >= max_pull_requests:
                                pages_remaining = False

                            if max_created_at:
                                pr_created_at = datetime.fromisoformat(
                                    prs[-1]["created_at"].replace("Z", "+00:00")
                                )
                                if pr_created_at <= max_created_at:
                                    pages_remaining = False
                            if min_created_at:
                                pr_created_at = datetime.fromisoformat(
                                    prs[-1]["created_at"].replace("Z", "+00:00")
                                )
                                if pr_created_at < min_created_at:
                                    pages_remaining = False
                        page_number += 1

                    for pr_index, pr in enumerate(prs):
                        self.logger.info(f"PR DETAILS:\n{pr}")
                        if max_pull_requests and pr_index >= max_pull_requests:
                            break

                        pr_created_at = datetime.fromisoformat(
                            pr["created_at"].replace("Z", "+00:00")
                        )

                        if min_created_at and pr_created_at < min_created_at:
                            break

                        if not max_created_at or pr_created_at <= max_created_at:
                            if (include_merged and pr.get("'merge_commit_sha'")) or pr[
                                "state"
                            ] == (status or "closed"):
                                closed_prs_list.append(
                                    GithubPullRequest(
                                        pull_request_number=pr["number"],
                                        repo=repo["name"],
                                        title=pr.get("title") or "No Title",
                                        created_at=(
                                            datetime.fromisoformat(
                                                pr["created_at"].replace("Z", "+00:00")
                                            )
                                            if pr.get("created_at")
                                            else None
                                        ),
                                        closed_at=(
                                            datetime.fromisoformat(
                                                pr["closed_at"].replace("Z", "+00:00")
                                            )
                                            if pr.get("closed_at")
                                            else None
                                        ),
                                        updated_at=(
                                            datetime.fromisoformat(
                                                pr["updated_at"].replace("Z", "+00:00")
                                            )
                                            if pr.get("updated_at")
                                            else None
                                        ),
                                        html_url=pr.get("html_url") or "No URL",
                                        diff_url=pr.get("diff_url") or "No URL",
                                        user=pr.get("user", {}).get("login")
                                        or "No User",
                                        state=pr.get("state"),
                                        body=pr.get("body"),
                                    )
                                )

                # sort the result across all repos
                def sort_func(pr1: GithubPullRequest) -> Union[datetime, int, None]:
                    if sort_by == "created":
                        return pr1.created_at
                    elif sort_by == "updated":
                        return pr1.updated_at
                    else:
                        return pr1.created_at

                closed_prs_list = sorted(
                    closed_prs_list,
                    key=sort_func,  # type: ignore[arg-type]
                    reverse=(
                        True
                        if not sort_by_direction or sort_by_direction == "desc"
                        else False
                    ),
                )
                closed_prs_list = (
                    closed_prs_list[:max_pull_requests]
                    if max_pull_requests
                    else closed_prs_list
                )

                return GithubPullRequestResult(
                    pull_requests=closed_prs_list, query=query, error=None
                )

            except Exception as e:
                self.logger.error(f"Error retrieving PRs: {e}")
                return GithubPullRequestResult(
                    pull_requests=[], query=query, error=str(e)
                )

    # noinspection PyMethodMayBeStatic
    def summarize_prs_by_engineer(
        self, *, pull_requests: List[GithubPullRequest]
    ) -> Dict[str, GithubPullRequestPerContributorInfo]:
        """
        Summarize pull requests by engineer.

        Args:
            pull_requests (List[GithubPullRequest]): List of pull requests

        Returns:
            Dict[str, GithubPullRequestPerContributorInfo]: Summary of PRs by engineer
        """
        engineer_pr_counts: Dict[str, GithubPullRequestPerContributorInfo] = {}

        for pr in pull_requests:
            engineer = pr.user
            info = engineer_pr_counts.get(engineer)

            if info is None:
                engineer_pr_counts[engineer] = GithubPullRequestPerContributorInfo(
                    contributor=engineer,
                    pull_request_count=1,
                    repos=[pr.repo],
                )
            else:
                info.pull_request_count += 1
                if info.repos:
                    if pr.repo not in info.repos:
                        info.repos.append(pr.repo)
                else:
                    info.repos = [pr.repo]

        # Sort engineer_pr_counts by PR count
        return dict(
            sorted(
                engineer_pr_counts.items(),
                key=lambda item: item[1].pull_request_count,
                reverse=True,
            )
        )

    # noinspection PyMethodMayBeStatic
    def parse_pr_url(self, *, pr_url: str) -> Dict[str, Union[str, int]]:
        """
        Parse GitHub PR URL to extract repository and PR details.

        Args:
            pr_url (str): Full GitHub PR URL

        Returns:
            Dict containing owner, repo, and PR number

        Raises:
            ValueError: If URL is not a valid GitHub PR URL
        """
        parsed_url = urlparse(pr_url)

        # Support both github.com and GitHub Enterprise URLs
        hostname = parsed_url.hostname
        if not (
            hostname in ["github.com", "www.github.com"]
            or (hostname and hostname.endswith(".githubenterprise.com"))
        ):
            raise ValueError("Invalid GitHub URL")

        # Regex to match GitHub PR URL pattern
        match = re.match(r"/([^/]+)/([^/]+)/pull/(\d+)", parsed_url.path)

        if not match:
            raise ValueError("Invalid GitHub PR URL format")

        return {
            "owner": match.group(1),
            "repo": match.group(2),
            "pr_number": int(match.group(3)),
        }

    async def get_pr_diff_content(self, *, pr_url: str) -> str:
        """
        Async method to fetch the actual diff content for a given GitHub PR URL.

        Args:
            pr_url (str): Full GitHub PR URL

        Returns:
            str: The raw diff content of the PR
        """

        assert self.org_name, "Organization name is required"
        assert self.github_access_token, "GitHub access token is required"

        async with self.http_client_factory.create_http_client(
            base_url=self.base_url
        ) as client:
            try:
                # Parse the PR URL
                pr_details: Dict[str, Any] = self.parse_pr_url(pr_url=pr_url)

                # Construct diff URL
                pr_url = f"{self.base_url}/repos/{pr_details['owner']}/{pr_details['repo']}/pulls/{pr_details['pr_number']}"
                headers: Dict[str, str] = {
                    "Authorization": f"Bearer {self.github_access_token}",
                    "Accept": "application/vnd.github.v3.diff",  # Specific media type for diff
                    "X-GitHub-Api-Version": "2022-11-28",  # Specify API version
                    "User-Agent": "AsyncGithubPullRequestHelper",
                }
                # Fetch PR details
                pr_response: Response = await client.get(
                    url=pr_url, headers=headers, follow_redirects=True
                )
                pr_response.raise_for_status()

                # self.logger.info(f"PR Response:\n{pr_response.text}")

                return pr_response.text

            except Exception as e:
                self.logger.error(f"Error fetching PR diff content: {e}")
                raise

    def export_results(
        self,
        *,
        pr_counts: Dict[str, GithubPullRequestPerContributorInfo],
        output_file: str,
    ) -> None:
        """
        Export PR count results to console and optional file.

        Args:
            pr_counts (Dict[str, GithubPullRequestPerContributorInfo]): PR counts by engineer
            output_file (Optional[str]): Path to output file
        """
        assert output_file, "Output file path is required"
        assert pr_counts, "PR counts are required"

        try:
            with open(output_file, "w") as f:
                f.write(self.export_results_as_csv(pr_counts=pr_counts))
            self.logger.info(f"Results exported to {output_file}")
        except IOError as e:
            self.logger.error(f"Failed to export results: {e}")

    # noinspection PyMethodMayBeStatic
    def export_results_as_csv(
        self,
        *,
        pr_counts: Dict[str, GithubPullRequestPerContributorInfo],
    ) -> str:
        """
        Export PR count results to console and optional file.

        Args:
            pr_counts (Dict[str, GithubPullRequestPerContributorInfo]): PR counts by engineer
        """

        result: str = "Contributor,PullRequests,Repos\n"
        for engineer, info in pr_counts.items():
            repos_text: str = " | ".join(info.repos) if info.repos else ""
            result += f'{engineer},{info.pull_request_count},"{repos_text}"\n'
        return result

    async def get_pr_info(self, *, pr_url: str) -> GithubPullRequest:
        """
        Async method to fetch information for a given GitHub PR URL.

        Args:
            pr_url (str): Full GitHub PR URL

        Returns:
            GithubPullRequest: The pull request information
        """
        assert self.org_name, "Organization name is required"
        assert self.github_access_token, "GitHub access token is required"

        async with self.http_client_factory.create_http_client(
            base_url=self.base_url
        ) as client:
            try:
                # Parse the PR URL
                pr_details: Dict[str, Any] = self.parse_pr_url(pr_url=pr_url)

                # Construct PR URL
                pr_url = f"{self.base_url}/repos/{pr_details['owner']}/{pr_details['repo']}/pulls/{pr_details['pr_number']}"
                headers: Dict[str, str] = {
                    "Authorization": f"Bearer {self.github_access_token}",
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "AsyncGithubPullRequestHelper",
                }
                # Fetch PR details
                pr_response: Response = await client.get(
                    url=pr_url, headers=headers, follow_redirects=True
                )
                pr_response.raise_for_status()
                pr_data = pr_response.json()

                return GithubPullRequest(
                    pull_request_number=pr_data["number"],
                    repo=pr_data["base"]["repo"]["name"],
                    user=pr_data["user"]["login"],
                    title=pr_data["title"],
                    created_at=datetime.fromisoformat(
                        pr_data["created_at"].replace("Z", "+00:00")
                    ),
                    closed_at=(
                        datetime.fromisoformat(
                            pr_data["closed_at"].replace("Z", "+00:00")
                        )
                        if pr_data.get("closed_at")
                        else None
                    ),
                    updated_at=datetime.fromisoformat(
                        pr_data["updated_at"].replace("Z", "+00:00")
                    ),
                    html_url=pr_data["html_url"],
                    diff_url=pr_data.get("diff_url"),
                    state=pr_data["state"],
                    body=pr_data.get("body"),
                )

            except Exception as e:
                self.logger.error(f"Error fetching PR information: {e}")
                raise
