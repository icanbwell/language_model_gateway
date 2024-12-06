import aiohttp
from langchain.tools import BaseTool

from language_model_gateway.gateway.utilities.html_to_markdown_converter import (
    HtmlToMarkdownConverter,
)


class URLToMarkdownTool(BaseTool):
    """
    LangChain-compatible tool for downloading the content of a URL and converting it to Markdown.
    """

    name: str = "url_to_markdown"
    description: str = (
        "Fetches the content of a webpage from a given URL and converts it to Markdown format. "
        "Provide the URL as input. The tool will return the main content of the page formatted as Markdown."
    )

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
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    html_content = await response.text()

            return await HtmlToMarkdownConverter.get_markdown_from_html_async(
                html_content=html_content
            )
        except Exception as e:
            raise ValueError(f"Failed to fetch or process the URL: {str(e)}")
