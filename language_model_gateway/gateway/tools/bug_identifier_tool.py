import logging
from typing import Type, Literal, Tuple, Optional
import os
from pydantic import BaseModel, Field
from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool
from language_model_gateway.gateway.file_managers.file_manager import FileManager
from language_model_gateway.gateway.file_managers.file_manager_factory import (
    FileManagerFactory,
)
from starlette.responses import Response, StreamingResponse
from language_model_gateway.gateway.utilities.s3_url import S3Url

logger = logging.getLogger(__name__)


class BugIdentifierModel(BaseModel):
    """
    Model to identify bug root cause
    """

    error_details: Optional[str] = Field(
        default=None,
        description=(
            "Error details to identify bug root cause to search through the CSV retrieved or web"
            "PARSING INSTRUCTION: Extract exact error details from the query. "
        ),
    )
    use_verbose_logging: Optional[bool] = Field(
        default=False,
        description="Whether to enable verbose logging",
    )


class BugIdentifierTool(ResilientBaseTool):
    """
    The BugIdentifierTool is designed to provide intelligent bug resolution support by processing
    a centralized bug database stored in S3. This tool specializes in matching user-reported
    error messages against a comprehensive bug resolution database to provide accurate,
    actionable solutions.
    """

    name: str = "bug_identifier"

    description: str = """
    Features:
    - Accepts error messages or stack traces from various input formats
    - Retrieves bug resolution data from a centralized CSV file in S3
    - Performs comprehensive matching against error descriptions in the CSV
    - Extracts root cause, Jira ticket ID, and resolution details
    - Implements fallback web search mechanism for unresolved errors
    - Generates structured resolution output with confidence scoring
    - Supports multiple error input types:
      * Multi-line stack traces
      * Single error lines
      * Generic human-language error descriptions

    Matching Capabilities:
    - Semantic error message matching
    - Keyword-based searching in CSV database
    - Partial and context-aware matching techniques
    - Automatic web search for unmatched errors

    Output Characteristics:
    - Provides solution from internal CSV database
    - Fallback to web search if no direct match found
    - Generates structured resolution format
    - Includes confidence level assessment
    """

    args_schema: Type[BaseModel] = (
        BugIdentifierModel  # Should be the input parameters class you created above
    )
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"
    file_manager_factory: FileManagerFactory
    bug_csv_file_path: Optional[str] = os.environ.get("BUG_FILE_S3_URL")

    async def _arun(
        self, error_details: Optional[str], use_verbose_logging: Optional[bool] = None
    ) -> Tuple[str, str]:
        """
        Asynchronously identify bug solution based on error message

        Args:
            error_details: The exact error message to match
            use_verbose_logging: Flag to enable verbose logging

        Returns:
            Tuple of CSV file content (or error message) and artifact description
        """
        assert self.bug_csv_file_path, "Set BUG_FILE_S3_URL in env"

        # Parse S3 URL
        s3_uri = S3Url(self.bug_csv_file_path)
        bucket_name = s3_uri.bucket
        file_name = s3_uri.key

        # Get file manager
        file_manager: FileManager = self.file_manager_factory.get_file_manager(
            folder=self.bug_csv_file_path
        )

        # Download the file from the S3 bucket
        response: StreamingResponse | Response = await file_manager.read_file_async(
            folder=bucket_name, file_path=file_name
        )
        artifact: Optional[str] = None

        # Check if the response is successful
        if not isinstance(response, StreamingResponse):
            content, artifact = (
                "Failed to retrieve the file",
                f"Error retrieving file: {response}",
            )
        else:
            # Extract content from the file
            content = await self._extract_content(response)
            artifact = f'BugIdentifierAgent: File successfully fetched for error "{error_details}"'
            if use_verbose_logging:
                artifact += f"\n```{content}```"

        return content, artifact

    def _run(
        self,
        error_details: Optional[str] = None,
        use_verbose_logging: Optional[bool] = None,
    ) -> Tuple[str, str]:
        """
        Synchronous version of the tool (falls back to async implementation).

        Raises:
            NotImplementedError: Always raises to enforce async usage
        """
        raise NotImplementedError("Use async version of this tool")

    async def _extract_content(self, response: StreamingResponse) -> str:
        """Extracts and returns content from a streaming response."""
        extracted_content = ""
        async for chunk in response.body_iterator:
            # Decode the chunk, assuming it is UTF-8 encoded
            extracted_content += chunk.decode("utf-8")  # type: ignore

        return extracted_content
