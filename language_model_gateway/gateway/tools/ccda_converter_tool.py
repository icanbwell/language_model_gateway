from language_model_gateway.gateway.file_managers.file_manager import FileManager
from language_model_gateway.gateway.file_managers.file_manager_factory import (
    FileManagerFactory,
)

from pydantic import BaseModel, Field
from typing import Type, Tuple, Literal
from starlette.responses import Response, StreamingResponse

from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool
from language_model_gateway.gateway.utilities.s3_url import S3Url


class CCDAExtractorModel(BaseModel):
    """
    Input model for CCDA conveter tool
    example:
    {
        uri: s3://bwell-dev-ingestion-ue1/testing/cw-ccda-2.16.840.1.113883.3.3330.8889429.1670.1^89765..1.txt
    }
    """

    url: str = Field(
        default=None,
        description="S3 uri for the file which will contain the CCDA data",
    )


class CCDAExtractorTool(ResilientBaseTool):
    """
    This tool is designed to take s3 uri of a file as input, get the file, reads its content and 
    return the ccda data for further conversions.
    """

    name: str = "ccda_to_fhir_converter"

    description: str = """
    The CCDAExtractorTool is designed to convert ccda data to fhir r4b standard format
    by processing ccad files stored in S3 in .txt format.
    Features:
    - Accepts an s3 file URL from user.
    - Extracts all the data in xml format.
    - Return the ccda data in xml format for further processing.
    - the xml data will futher be converted to fhir f4b standard format.
    """

    args_schema: Type[BaseModel] = (
        CCDAExtractorModel  # Should be the input parameters class you created above
    )
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"
    file_manager_factory: FileManagerFactory


    async def _arun(self, url: str) -> Tuple[str, str]:

        # Create a file manager instance
        file_manager: FileManager = self.file_manager_factory.get_file_manager(
            folder=url
        )
        s3_uri = S3Url(url)
        bucket_name = s3_uri.bucket
        file_name = s3_uri.key

        # read the file from S3 
        response: StreamingResponse | Response = await file_manager.read_file_async(
            folder=bucket_name, file_path=file_name
        )

        # Check if the response is successful
        if not isinstance(response, StreamingResponse):
            return "Failed to retrieve the file", f"Error retrieving file: {response}"

        # Extract content from the file
        content = await file_manager.extract_content(response)
        return content, "File successfully fetched"

    def _run(self, url: str) -> Tuple[str, str]:
        """
        Synchronous version of the tool (falls back to async implementation).
        Raises:
            NotImplementedError: Always raises to enforce async usage
        """
        raise NotImplementedError("Use async version of this tool")
