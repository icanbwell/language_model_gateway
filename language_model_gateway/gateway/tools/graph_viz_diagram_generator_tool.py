import logging
import os
from typing import Type, Literal, Tuple, Optional
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


class GraphVizDiagramGeneratorToolInput(BaseModel):
    dot_input: str = Field(
        description="a string describing the nodes and edges in DOT format. "
        "For example:\n"
        "digraph G {\n"
        "  A -> B;\n"
        "  B -> C;\n"
        "  C -> A;\n"
        "}"
    )


class GraphVizDiagramGeneratorTool(ResilientBaseTool):
    """
    LangChain-compatible tool for generating a diagram using Graphviz.
    """

    name: str = "graphviz_diagram_generator"
    description: str = (
        "Generate a diagram using Graphviz. "
        "Provide input as a string describing the nodes and edges in DOT format. "
        "For example:\n"
        "digraph G {\n"
        "  A -> B;\n"
        "  B -> C;\n"
        "  C -> A;\n"
        "}"
        "This will generate a directed graph with three nodes: A, B, and C."
    )
    args_schema: Type[BaseModel] = GraphVizDiagramGeneratorToolInput
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"
    file_manager_factory: FileManagerFactory

    def _run(self, dot_input: str) -> Tuple[str, str]:
        """
        Run the tool to generate a diagram from DOT input.
        :param dot_input: The DOT description of the graph.
        :return: The path to the generated diagram.
        """
        raise NotImplementedError("Call the asynchronous version of the tool")

    async def _arun(self, dot_input: str) -> Tuple[str, str]:
        """
        Asynchronous version of the tool.
        :param dot_input: The DOT description of the graph.
        :return: The path to the generated diagram.
        """
        # For simplicity, call the synchronous version
        try:
            # Create a Graphviz object
            dot = Digraph(format="png")
            # Parse the DOT input
            for line in dot_input.strip().split("\n"):
                if "->" in line or "--" in line:
                    # Add edges
                    edge = line.replace(";", "").strip()
                    nodes = edge.split("->" if "->" in edge else "--")
                    dot.edge(nodes[0].strip(), nodes[1].strip())
                elif (
                    line.strip()
                    and not line.startswith("digraph")
                    and not line.endswith("}")
                ):
                    # Add standalone nodes
                    node = line.replace(";", "").strip()
                    dot.node(node)

            # Render the diagram
            image_generation_path_ = os.environ["IMAGE_GENERATION_PATH"]
            assert image_generation_path_, (
                "IMAGE_GENERATION_PATH environment variable is not set"
            )
            image_file_name: str = f"{uuid4()}.png"

            # dot.render(output_file, cleanup=True)
            # Create a BytesIO object to store the image
            # image_bytes = BytesIO()

            # Render the diagram directly to bytes
            image_data: bytes = dot.pipe(format="png")
            file_manager: FileManager = self.file_manager_factory.get_file_manager(
                folder=image_generation_path_
            )
            file_path: Optional[str] = await file_manager.save_file_async(
                file_data=image_data,
                folder=image_generation_path_,
                filename=image_file_name,
            )
            if file_path is None:
                return (
                    "Failed to save image to disk",
                    f"GraphVizDiagramGeneratorAgent: Failed to save image to disk from prompt: {dot_input}",
                )

            url: Optional[str] = UrlParser.get_url_for_file_name(image_file_name)
            if url is None:
                return (
                    "Failed to save image to disk",
                    f"GraphVizDiagramGeneratorAgent: Failed to save image to disk from prompt: {dot_input}",
                )

            artifact: str = f"GraphVizDiagramGeneratorAgent: Generated image: <{url}> "
            return url, artifact
        except Exception as e:
            raise ValueError(f"Failed to generate diagram: {str(e)}")
