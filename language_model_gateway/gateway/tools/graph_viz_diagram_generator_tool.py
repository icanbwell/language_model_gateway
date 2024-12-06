import logging
from pathlib import Path

from graphviz import Digraph
from langchain.tools import BaseTool

from language_model_gateway.gateway.utilities.image_generation_helper import (
    ImageGenerationHelper,
)

logger = logging.getLogger(__name__)


class GraphVizDiagramGeneratorTool(BaseTool):
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

    def _run(self, dot_input: str) -> str:
        """
        Run the tool to generate a diagram from DOT input.
        :param dot_input: The DOT description of the graph.
        :return: The path to the generated diagram.
        """
        try:
            output_file: Path = ImageGenerationHelper.get_full_path()
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
            dot.render(output_file, cleanup=True)
            return ImageGenerationHelper.get_url_for_file_name(output_file)
        except Exception as e:
            raise ValueError(f"Failed to generate diagram: {str(e)}")

    async def _arun(self, dot_input: str) -> str:
        """
        Asynchronous version of the tool.
        :param dot_input: The DOT description of the graph.
        :return: The path to the generated diagram.
        """
        # For simplicity, call the synchronous version
        return self._run(dot_input)
