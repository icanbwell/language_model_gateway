import json
from os import environ
from uuid import uuid4

from language_model_gateway.gateway.file_managers.file_manager import FileManager
from language_model_gateway.gateway.file_managers.file_manager_factory import (
    FileManagerFactory,
)

from pydantic import BaseModel, Field
from typing import Type, Tuple, Literal, Dict, Any

from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool


class SendFHIRDataToS3Model(BaseModel):
    """
    Input model for CCDA conveter tool
    example:
    {
        uri: s3://bwell-dev-ingestion-ue1/testing/cw-ccda-2.16.840.1.113883.3.3330.8889429.1670.1^89765..1.txt
    }
    """

    fhir_data: Dict[str, Any] = Field(
        default=None,
        description="converted fhir data",
    )


class SendFHIRDataToS3Tool(ResilientBaseTool):
    """
    This tool is designed to take s3 uri of a file as input, get the file, reads its content and 
    return the ccda data for further conversions.
    """

    name: str = "push_fhir_bundle_to_s3"

    description: str = """
    After the ccda data got converted to fhir r4b format and is received, now send the fhir data back to s3 on the url formed.
    Features:
    - Accept a dictonary of fhir bundle data which is formed after ccda data is converted to fhir.
    - form a path for where the fhir data will be sent to s3.
    - add fhir data to text file.
    - push data to s3.
    """

    args_schema: Type[BaseModel] = (
        SendFHIRDataToS3Model  # Should be the input parameters class you created above
    )
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"
    file_manager_factory: FileManagerFactory

    # Convert FHIR bundle to formatted text
    def convert_fhir_to_text(fhir_bundle):
        # Simply convert the JSON to a nicely formatted string
        return json.dumps(fhir_bundle, indent=2).encode('utf-8')

    async def _arun(self, fhir_bundle: Dict[str, Any]) -> Tuple[str, str]:
        if not environ.get("S3_FHIR_DATA_PATH"):
            return "s3 path to save data is not provided", "s3 path missing"

        # Create a file manager instance
        file_manager: FileManager = self.file_manager_factory.get_file_manager(
            folder=environ["S3_FHIR_DATA_PATH"]
        )

        text_content = SendFHIRDataToS3Tool.convert_fhir_to_text(fhir_bundle)
        # SendFHIRDataToS3Tool.save_to_text_file(text_content, 'fhir_bundle.txt')

        # read the file from S3 
        file_path = await file_manager.save_file_async(
            file_data=text_content,
            folder=environ["S3_FHIR_DATA_PATH"],
            file_name = f"{uuid4()}.txt",
            content_type="application/json"
        )

        # Check if the response is successful
        if file_path is None:
                return (
                    "Failed to save fhir data to s3",
                    "Failed to save fhir data to s3",
                )

        return file_path, "File successfully saved to s3"

    def _run(self, url: str) -> Tuple[str, str]:
        """
        Synchronous version of the tool (falls back to async implementation).
        Raises:
            NotImplementedError: Always raises to enforce async usage
        """
        raise NotImplementedError("Use async version of this tool")
