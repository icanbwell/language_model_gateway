import logging
from typing import Type

import httpx
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from language_model_gateway.gateway.utilities.html_to_markdown_converter import (
    HtmlToMarkdownConverter,
)


logger = logging.getLogger(__name__)


class URLToMarkdownToolInput(BaseModel):
    url: str = Field(description="url of the webpage to scrape")


class URLToMarkdownTool(BaseTool):
    """
    LangChain-compatible tool for downloading the content of a URL and converting it to Markdown.
    """

    name: str = "url_to_markdown"
    description: str = (
        "Fetches the content of a webpage from a given URL and converts it to Markdown format. "
        "Provide the URL as input. The tool will return the main content of the page formatted as Markdown."
    )
    args_schema: Type[BaseModel] = URLToMarkdownToolInput

    def _run(self, url: str) -> str:
        """
        Synchronous version of the tool (falls back to async implementation).
        :param url: The URL of the webpage to fetch.
        :return: The content of the webpage in Markdown format.
        """
        raise NotImplementedError("Use async version of this tool")

    async def _arun(self, url: str) -> str:
        """
        Asynchronous version of the tool.
        :param url: The URL of the webpage to fetch.
        :return: The content of the webpage in Markdown format.
        """
        logger.info(f"Fetching and converting URL to Markdown: {url}")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                html_content = response.text

            content: str = await HtmlToMarkdownConverter.get_markdown_from_html_async(
                html_content=html_content
            )
            logger.info(
                f"====== Scraped {url} ======\n{content}\n====== End of Scraped Markdown ======"
            )
            return content
        except Exception as e:
            return f"Failed to fetch or process the URL: {str(e)}"
