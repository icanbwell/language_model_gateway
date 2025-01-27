import logging
from typing import Dict, List, Type, Literal, Tuple, Optional
import os, json
from pathlib import Path
from pydantic import BaseModel, Field
from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool
from language_model_gateway.gateway.file_managers.file_manager import FileManager
from language_model_gateway.gateway.file_managers.file_manager_factory import (
    FileManagerFactory,
)
from starlette.responses import Response, StreamingResponse
from language_model_gateway.gateway.utilities.s3_url import S3Url

logger = logging.getLogger(__name__)


class SystemCodesCrossWalkModel(BaseModel):
    """
    Input Model for System Code Crosswalk tool.
    """
    input: Optional[str] = Field(
        default=None,
        description=(
            "system and code or display to get code display for an expected system"
            "PARSING INSTRUCTION: Extract exact output from the query."
        ),
    )
    use_verbose_logging: Optional[bool] = Field(
        default=False,
        description="Whether to enable verbose logging",
    )


class SystemCodesCrossWalkTool(ResilientBaseTool):

    name: str = "system_codes_crosswalk"

    description: str = """
    Features:
    - Accepts input messages in various input formats
    - Read the training_dataset from local file system
    - Performs comprehensive matching against input with tarining dataset
    - Implements fallback web search mechanism for unresolved inputs
    - Generates structured resolution output with confidence scoring
    - Supports multiple input types:
      * Multi-line input
      * single json type object
      * list of multiple json type input
      * Generic human-language input descriptions

    Matching Capabilities:
    - Semantic input message matching with training data
    - Keyword-based searching with training data
    - Partial and context-aware matching techniques
    - Automatic web search for unmatched input
    Output Characteristics:
    - Provides solution based on given dataset 
    - Fallback to web search if no direct match found
    - Generates structured resolution format
    - Includes confidence level assessment
    """

    args_schema: Type[BaseModel] = (
        SystemCodesCrossWalkModel  # Should be the input parameters class you created above
    )
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"
    file_manager_factory: FileManagerFactory
    training_data_folder: Path = Path(__file__).parent.joinpath("./code_system_training_data")
    training_data_path: Path = Path(__file__).parent.joinpath("./code_system_training_data/training_dataset.json")


    async def _arun(
        self, input: Optional[str], use_verbose_logging: Optional[bool] = None
    ) -> Tuple[str, str]:
        """
        Asynchronously identify bug solution based on error message
        Args:
            input: The exact error message to match
            use_verbose_logging: Flag to enable verbose logging
        Returns:
            Tuple of CSV file content (or error message) and artifact description
        """

        # Parse input
        training_data: List[Dict[str, str]]
        with open(self.training_data_path, "r") as file:
            training_data = json.loads(file.read())

        # # Get file manager
        file_manager: FileManager = self.file_manager_factory.get_file_manager(
            folder=self.training_data_path
        )

        # Download the file from the S3 bucket
        response: StreamingResponse | Response = await file_manager.read_file_async(
            folder=self.training_data_folder, file_path="training_dataset.json"
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
            artifact = f'BugIdentifierAgent: File successfully fetched for given input: {input}'
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