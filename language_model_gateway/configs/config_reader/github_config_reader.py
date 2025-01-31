import asyncio
import logging
import os
import time

import httpx
import json
from typing import List, Tuple, Optional, Any, Dict
from urllib.parse import urlparse, unquote

from language_model_gateway.configs.config_schema import ChatModelConfig

logger = logging.getLogger(__name__)


class GitHubConfigReader:
    def __init__(self) -> None:
        """
        Initialize the async GitHub config reader

        """
        self.github_token: Optional[str] = os.environ.get("GITHUB_TOKEN")
        self.max_retries: int = 5
        self.base_delay: int = 1  # Base delay in seconds

    @staticmethod
    def parse_github_url(github_url: str) -> Tuple[str, str, str]:
        """
        Parse a GitHub URL into repository, path, and branch components

        Args:
            github_url: Full GitHub URL (e.g., https://github.com/owner/repo/tree/branch/path)

        Returns:
            Tuple of (repo, path, branch)
        """
        parsed = urlparse(github_url)

        if parsed.netloc != "github.com":
            raise ValueError(f"Not a GitHub URL: {github_url}")

        # Split the path into components
        parts = [p for p in parsed.path.split("/") if p]

        if len(parts) < 4 or parts[2] != "tree":
            raise ValueError(
                "Invalid GitHub URL format. Expected format: "
                "https://github.com/owner/repo/tree/branch/path"
            )

        owner = parts[0]
        repo = parts[1]
        branch = parts[3]
        path = "/".join(parts[4:])

        # Decode URL-encoded characters
        path = unquote(path)

        return f"{owner}/{repo}", path, branch

    async def _make_request(
        self,
        *,
        client: httpx.AsyncClient,
        url: str,
        headers: Dict[str, str],
        retry_count: int = 0,
    ) -> httpx.Response:
        """
        Make an HTTP request with rate limit handling and retries
        """
        try:
            response = await client.get(url, headers=headers)

            # Check for rate limit
            if (
                response.status_code == 403
                and "rate limit exceeded" in response.text.lower()
            ):
                remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
                reset_time = int(response.headers.get("X-RateLimit-Reset", 0))

                if remaining == 0 and reset_time:
                    wait_time = reset_time - time.time()
                    if wait_time > 0:
                        logger.warning(
                            f"Rate limit exceeded. Waiting for {wait_time:.2f} seconds"
                        )
                        await asyncio.sleep(wait_time)
                        return await self._make_request(
                            client=client,
                            url=url,
                            headers=headers,
                            retry_count=retry_count,
                        )

            # Handle other 4xx/5xx errors with exponential backoff
            if response.status_code >= 400:
                if retry_count >= self.max_retries:
                    response.raise_for_status()

                delay = self.base_delay * (2**retry_count)  # Exponential backoff
                logger.warning(
                    f"Request failed with status {response.status_code}. Retrying in {delay} seconds..."
                )
                await asyncio.sleep(delay)
                return await self._make_request(
                    client=client, url=url, headers=headers, retry_count=retry_count + 1
                )

            return response

        except httpx.RequestError as e:
            if retry_count >= self.max_retries:
                raise
            delay = self.base_delay * (2**retry_count)
            logger.warning(f"Request error: {str(e)}. Retrying in {delay} seconds...")
            await asyncio.sleep(delay)
            return await self._make_request(
                client=client, url=url, headers=headers, retry_count=retry_count + 1
            )

    async def read_model_configs(self, *, github_url: str) -> List[ChatModelConfig]:
        """
        Read model configurations from JSON files stored in a GitHub repository
        """
        logger.info(f"Reading model configurations from GitHub: {github_url}")

        # Parse the GitHub URL
        repo_url, path, branch = self.parse_github_url(github_url)
        try:
            models = await self._read_model_configs(
                repo_url=repo_url,
                path=path,
                branch=branch,
                github_token=self.github_token,
            )
            # Store in cache
            return models
        except Exception as e:
            logger.error(f"Error reading model configurations from Github: {str(e)}")
            logger.exception(e, stack_info=True)
            return []

    async def _read_model_configs(
        self, *, repo_url: str, path: str, branch: str, github_token: Optional[str]
    ) -> List[ChatModelConfig]:
        """
        Read model configurations from JSON files stored in a GitHub repository

        Args:
            repo_url: The GitHub repository URL (format: 'owner/repo')
            path: The path within the repository where config files are stored
            branch: The branch to read from
            github_token: Optional GitHub token for private repositories
        """
        assert repo_url
        assert path
        assert branch

        logger.info(f"Reading model configurations from GitHub: {repo_url}/{path}")
        configs: List[ChatModelConfig] = []

        async with httpx.AsyncClient() as client:
            try:
                # Construct the GitHub API URL to list contents
                api_url = f"https://api.github.com/repos/{repo_url}/contents/{path}?ref={branch}"

                headers = (
                    {"Authorization": f"token {github_token}"} if github_token else {}
                )
                headers["Accept"] = "application/vnd.github.v3+json"

                # Get the list of files with rate limit handling
                response = await self._make_request(
                    client=client, url=api_url, headers=headers
                )

                response.raise_for_status()

                # Process each file in the directory
                items = response.json()
                json_files = [
                    item
                    for item in items
                    if item["type"] == "file" and item["name"].endswith(".json")
                ]

                async def fetch_and_parse_config(
                    item: Dict[str, Any],
                ) -> Optional[ChatModelConfig]:
                    try:
                        raw_url = item["download_url"]
                        file_response = await client.get(raw_url, headers=headers)
                        file_response.raise_for_status()

                        data = file_response.json()
                        return ChatModelConfig(**data)
                    except httpx.RequestError as e:
                        logger.error(f"Error reading file {item['name']}: {str(e)}")
                    except json.JSONDecodeError as e:
                        logger.error(
                            f"Error parsing JSON from {item['name']}: {str(e)}"
                        )
                    except Exception as e:
                        logger.error(
                            f"Unexpected error processing {item['name']}: {str(e)}"
                        )
                    return None

                # Process all files concurrently
                tasks = [fetch_and_parse_config(item) for item in json_files]
                results = await asyncio.gather(*tasks)

                # Filter out None results and add valid configs to the list
                configs.extend([config for config in results if config is not None])
                # sort the configs by name
                configs.sort(key=lambda x: x.name)

                return configs

            except Exception as e:
                logger.error(f"Error reading configs from GitHub: {str(e)}")
                raise
