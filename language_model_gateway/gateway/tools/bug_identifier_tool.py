from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional, Tuple, Literal


class BugIdentifierModel(BaseModel):
    """
    Model to identify bug root cause
    """

    error_details: Optional[str] = Field(
        default=None,
        description=(
            "Optional error details to identify bug root cause and it's fix. "
            "PARSING INSTRUCTION: Extract exact error details from the query. "
        ),
    )


class BugIdentifierTool(ResilientBaseTool):
    """
    This tool can be used to debug an error if it has already been encountered and fixed earlier.
    If it is the first occurrence, then it will provide the error details and a probable fix.

    """

    name: str = "bug_identifier"

    description: str = """
    The BugIdentifierTool is designed to assist users by diagnosing errors or tracebacks provided by the user.
    
    Features:
    - Accepts user prompts containing error messages or stack trace details.
    - Integrates with business logic to access a CSV file stored on S3, containing columns for Jira ticket ID, description, and root cause.
    - Constructs a list of tuples from the CSV file, where each tuple contains a Jira ticket ID, description, and corresponding root cause.
    - Utilizes a language model API to analyze the user's prompt in conjunction with the CSV data, searching for matching entries based on the given error or traceback.
    - If a matching entry is found, it returns the associated Jira ticket ID and root cause to the user, aiding in the error resolution process.
    - In cases where no similar entry is found, the tool provides the user with the error details and suggests a probable fix, based on available data and analysis.

    This tool leverages advanced language processing and data integration to enhance debugging efficiency and streamline the problem-solving workflow.
    """

    args_schema: Type[BaseModel] = (
        BugIdentifierModel  # Should be the input parameters class you created above
    )
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"

    # You can define any other initialization parameters to your class.  These are not passed by the LLM but we can pass them
    # during initialization

    async def _arun(self, error_details: Optional[str] = None) -> Tuple[str, str]:
        # do your actual work here
        return (
            error_details if error_details else "No error parsed"
        ), "artifact that is not given to LLM but shown in the UI"

    def _run(self, error_details: Optional[str] = None) -> Tuple[str, str]:
        """
        Synchronous version of the tool (falls back to async implementation).

        Raises:
            NotImplementedError: Always raises to enforce async usage
        """
        raise NotImplementedError("Use async version of this tool")
