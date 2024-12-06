from typing import cast

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter


class HtmlToMarkdownConverter:
    @staticmethod
    async def get_markdown_from_html_async(*, html_content: str) -> str:
        soup = BeautifulSoup(html_content, "html.parser")
        return cast(str, MarkdownConverter().convert_soup(soup))

    @staticmethod
    async def get_plain_text_from_html_async(*, html_content: str) -> str:
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text content
        text = soup.get_text()

        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = " ".join(chunk for chunk in chunks if chunk)

        return text
