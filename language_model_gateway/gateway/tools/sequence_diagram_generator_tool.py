import logging
import os
import tempfile
from typing import Type, Literal, Tuple, Optional, List
from uuid import uuid4

from graphviz import Digraph
from pydantic import BaseModel, Field

from language_model_gateway.gateway.file_managers.file_manager import FileManager
from language_model_gateway.gateway.file_managers.file_manager_factory import (
    FileManagerFactory,
)
from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool
from language_model_gateway.gateway.utilities.url_parser import UrlParser

logger = logging.getLogger(__name__)


class SequenceDiagramInput(BaseModel):
    """
    Input model for sequence diagram generation

    Example input format:
    participants: ["Client", "Server", "Database"]
    interactions: [
        ["Client", "Server", "sendRequest()"],
        ["Server", "Database", "queryData()"],
        ["Database", "Server", "returnResults()"],
        ["Server", "Client", "processResponse()"]
    ]
    """

    participants: List[str] = Field(
        description="List of participants in the sequence diagram",
    )
    interactions: List[List[str]] = Field(
        description="List of interactions. Each interaction is [sender, receiver, message]",
    )
    title: Optional[str] = Field(
        default=None, description="Optional title for the sequence diagram"
    )


class SequenceDiagramGeneratorTool(ResilientBaseTool):
    """
    LangChain-compatible tool for generating sequence diagrams using Graphviz.
    """

    name: str = "sequence_diagram_generator"
    description: str = (
        "Generate a sequence diagram using Graphviz. "
        "Provide a list of participants and their interactions. "
        "Example:\n"
        "participants: ['Client', 'Server', 'Database']\n"
        "interactions: ["
        "  ['Client', 'Server', 'sendRequest()'],"
        "  ['Server', 'Database', 'queryData()']"
        "]"
    )
    args_schema: Type[BaseModel] = SequenceDiagramInput
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"
    file_manager_factory: FileManagerFactory

    def _run(
        self,
        participants: List[str],
        interactions: List[List[str]],
        title: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Synchronous method (not implemented)
        """
        raise NotImplementedError("Call the asynchronous version of the tool")

    async def _arun(
        self,
        participants: List[str],
        interactions: List[List[str]],
        title: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Asynchronous method to generate a sequence diagram
        """
        try:
            # Create a Graphviz Digraph for the sequence diagram
            dot = Digraph(
                "sequence_diagram",
                filename="sequence_diagram",
                node_attr={"shape": "box", "style": "filled", "fillcolor": "lightblue"},
            )

            # Set graph attributes for sequence diagram layout
            dot.attr(rankdir="TB")  # Top to Bottom layout
            dot.attr("node", shape="plaintext")

            # Add title if provided
            if title:
                dot.attr(label=title, labelloc="t", fontsize="16")

            # Create participant lifelines
            for participant in participants:
                dot.node(participant, participant)
                # Create vertical lifeline
                dot.edge(participant, participant, style="dotted", color="gray")

            # Add interactions
            for i, (sender, receiver, message) in enumerate(interactions):
                dot.edge(
                    sender,
                    receiver,
                    label=message,
                    style="solid",
                    color="black",
                    constraint="false",
                )

            # Render the diagram to bytes
            image_data: bytes = dot.pipe(format="png")

            # Generate a unique filename
            image_file_name: str = f"{uuid4()}.png"

            # Use file manager to save the file (if needed)
            image_generation_path_ = os.environ.get(
                "IMAGE_GENERATION_PATH", tempfile.gettempdir()
            )
            file_manager: FileManager = self.file_manager_factory.get_file_manager(
                folder=image_generation_path_
            )

            # Attempt to save the file
            file_path: Optional[str] = await file_manager.save_file_async(
                file_data=image_data,
                folder=image_generation_path_,
                filename=image_file_name,
            )
            if file_path is None:
                return (
                    "Failed to save image to disk",
                    "SequenceDiagramGeneratorTool: Failed to save image to disk ",
                )

            # Generate URL for the image
            url: Optional[str] = UrlParser.get_url_for_file_name(image_file_name)
            if url is None:
                return (
                    "Failed to save image to disk",
                    "SequenceDiagramGeneratorTool: Failed to save image to disk",
                )

            return (
                url,
                f"SequenceDiagramGeneratorTool: Generated sequence diagram <{url}> ",
            )

        except Exception as e:
            logger.error(f"Failed to generate sequence diagram: {str(e)}")
            raise ValueError(f"Failed to generate sequence diagram: {str(e)}")
