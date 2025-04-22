import logging
from typing import Optional, Type, Tuple, Literal
from pydantic import BaseModel, Field
from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool
from language_model_gateway.gateway.utilities.confluence.confluence_document import (
    ConfluenceDocument,
)
from language_model_gateway.gateway.utilities.confluence.confluence_helper import (
    ConfluenceHelper,
)

logger = logging.getLogger(__name__)


class ConfluencePageRetrieverAgentInput(BaseModel):
    """
    Input model for retrieving a specific Confluence page by ID.
    """

    page_id: str = Field(
        default="", description="The ID of the Confluence page to retrieve."
    )


class ConfluencePageRetriever(ResilientBaseTool):
    """
    A LangChain-compatible tool for retrieving a specific Confluence page by ID.
    """

    name: str = "confluence_page_retriever"
    description: str = (
        "Tool to retrieve a specific Confluence page by ID. "
        "USAGE TIPS: "
        "- Provide the Confluence page ID to retrieve the page details."
    )

    args_schema: Type[BaseModel] = ConfluencePageRetrieverAgentInput
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"

    confluence_helper: ConfluenceHelper

    async def _arun(
        self,
        page_id: str,
    ) -> Tuple[str, str]:
        """
        Asynchronous version of the Confluence Page by ID tool.

        Returns:
            Tuple of Confluence page text and artifact description
        """
        log_prefix: str = f"ConfluencePageRetriever: page_id={page_id}"

        try:
            confluence_page: Optional[
                ConfluenceDocument
            ] = await self.confluence_helper.retrieve_page_by_id(page_id=page_id)

            if not confluence_page:
                error_msg = "Error retrieving Confluence page: Page not found"
                error_artifact = log_prefix + " Retrieval Failed: Page not found"
                logger.error(error_msg)
                return error_msg, error_artifact

            full_text_display = (
                f"**Title**: {confluence_page.title}\n"
                f"**URL**: {confluence_page.url}\n"
                f"**Updated**: {confluence_page.updated_at}\n"
                f"**Author**: {confluence_page.author_name}\n"
            )

            full_text = (
                f"Id: {confluence_page.id}\n"
                f"{full_text_display}"
                f"Content: {confluence_page.content}\n"
            )

            artifact = log_prefix + f", Retrieved page {confluence_page.id}.\n\n"
            artifact += f"\n{full_text_display}"

            return full_text, artifact

        except Exception as e:
            error_msg = f"Error retrieving Confluence page: {str(e)}"
            error_artifact = log_prefix + " Retrieval Failed: " + str(e)
            logger.error(error_msg)
            return error_msg, error_artifact

    def _run(
        self,
        page_id: str,
    ) -> Tuple[str, str]:
        """
        Synchronous version of the Confluence Page by ID tool.

        Returns:
            Tuple of Confluence page text and artifact description
        """
        raise NotImplementedError("Use async version of this tool")
