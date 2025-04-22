import json
from datetime import datetime, timezone
import os
from os import makedirs, path
from pathlib import Path
from shutil import rmtree
from typing import Dict, List, Optional, Any

import pytest
from pytest_httpx import HTTPXMock

from language_model_gateway.container.simple_container import SimpleContainer
from language_model_gateway.gateway.api_container import get_container_async
from language_model_gateway.gateway.http.http_client_factory import HttpClientFactory
from language_model_gateway.gateway.utilities.environment_reader import (
    EnvironmentReader,
)
from language_model_gateway.gateway.utilities.environment_variables import (
    EnvironmentVariables,
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
from tests.gateway.mocks.mock_environment_variables import MockEnvironmentVariables


@pytest.mark.httpx_mock(
    should_mock=lambda request: os.environ["RUN_TESTS_WITH_REAL_LLM"] != "1"
)
async def test_github_get_summarized_pull_requests_from_one_repo(
    httpx_mock: HTTPXMock,
) -> None:
    print()
    data_dir: Path = Path(__file__).parent.joinpath("./")
    temp_folder = data_dir.joinpath("./temp")
    if path.isdir(temp_folder):
        rmtree(temp_folder)
    makedirs(temp_folder)

    test_container: SimpleContainer = await get_container_async()

    max_pull_requests = 2
    max_repos = 2
    if not EnvironmentReader.is_environment_variable_set("RUN_TESTS_WITH_REAL_LLM"):
        org_name: str = "icanbwell"
        access_token: Optional[str] = "fake_token"
        test_container.register(
            EnvironmentVariables, lambda c: MockEnvironmentVariables()
        )

        sample_content: Dict[str, Any] = {
            "name": "helix.pipelines",
            "full_name": "icanbwell/helix.pipelines",
            "private": False,
            "html_url": "",
            "description": "Helix Pipelines",
        }

        # org_name = "icanbwell"
        repo_name = "helix.pipelines"
        # repos_url = f"https://api.github.com/repos/{org_name}/{repo_name}"
        repos_url = f"https://api.github.com/repos/{org_name}/{repo_name}"

        httpx_mock.add_response(
            url=repos_url,
            method="GET",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "AsyncGithubPullRequestHelper",
            },
            content=json.dumps(sample_content).encode(),
            status_code=200,
        )

        # mock pull API
        pull_url: str = f"https://api.github.com/repos/{org_name}/{repo_name}/pulls?state=closed&sort=created&direction=desc&per_page={max_pull_requests}&page=1"
        sample_pull_content: List[Dict[str, Any]] = [
            {
                "url": "https://api.github.com/repos/icanbwell/helix.pipelines/pulls/1",
                "html_url": "",
                "diff_url": "",
                "number": 1,
                "state": "closed",
                "title": "PR 1",
                "user": {"login": "user1"},
                "created_at": "2024-09-01T00:00:00Z",
                "merged_at": "2024-09-02T00:00:00Z",
            },
            {
                "url": "https://api.github.com/repos/icanbwell/helix.pipelines/pulls/2",
                "html_url": "",
                "diff_url": "",
                "number": max_repos,
                "state": "closed",
                "title": "PR 2",
                "user": {"login": "user2"},
                "created_at": "2024-09-01T00:00:00Z",
                "merged_at": "2024-09-02T00:00:00Z",
            },
        ]
        httpx_mock.add_response(
            url=pull_url,
            method="GET",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
            },
            content=json.dumps(sample_pull_content).encode(),
            status_code=200,
        )
    else:
        # Get credentials from environment variables
        org_name = "icanbwell"  # os.getenv('GITHUB_ORG')
        access_token = os.getenv("GITHUB_TOKEN")

    if not org_name or not access_token:
        raise ValueError("Please set GITHUB_ORG and GITHUB_TOKEN environment variables")

    # Initialize PR counter
    pr_counter = GithubPullRequestHelper(
        org_name=org_name,
        access_token=access_token,
        http_client_factory=HttpClientFactory(),
    )

    try:
        # Get PR counts with optional parameters
        pull_request_result: GithubPullRequestResult = (
            await pr_counter.retrieve_closed_prs(
                max_repos=max_repos,  # Optional: limit repositories
                max_pull_requests=max_pull_requests,  # Optional: limit PRs
                min_created_at=datetime(
                    2024, 9, 1, tzinfo=timezone.utc
                ),  # Optional: minimum created date
                include_merged=True,  # Include merged PRs
                repo_name="helix.pipelines",
            )
        )
        pull_requests: List[GithubPullRequest] = pull_request_result.pull_requests
        pr_counts: Dict[str, GithubPullRequestPerContributorInfo] = (
            pr_counter.summarize_prs_by_engineer(pull_requests=pull_requests)
        )

        # Export results
        pr_counter.export_results(
            pr_counts=pr_counts,
            output_file=str(
                temp_folder.joinpath("pr_counts.tsv")
            ),  # Optional TSV export
        )

    except Exception as e:
        print(f"An error occurred: {e}")
