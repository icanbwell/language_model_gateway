import logging
import os
import tempfile
from typing import Type, Literal, Tuple, Optional, List, Dict, Union, Set
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


class FlowChartInput(BaseModel):
    """
    Input model for flow chart generation

    Example input:
    {
        "nodes": {
            "Start": {"style": {"shape": "oval", "color": "lightgreen"}},
            "Decision": {"style": {"shape": "diamond", "color": "lightyellow"}},
            "Process": {"style": {"shape": "box", "color": "lightblue"}}
        },
        "connections": [
            {"from": "Start", "to": "Decision", "label": "Begin"},
            {"from": "Decision", "to": "Process", "label": "Yes"},
            {"from": "Decision", "to": "End", "label": "No"}
        ],
        "title": "Simple Flow Chart"
    }
    """

    nodes: Dict[str, Dict[str, Union[str, Dict[str, str]]]] = Field(
        description='Dictionary of nodes with optional styling.  Example: "Start": {"style": {"shape": "oval", "color": "lightgreen"}},'
    )
    connections: List[Dict[str, str]] = Field(
        description='List of connections between nodes. Example: {"from": "Start", "to": "Decision", "label": "Begin"}'
    )
    title: Optional[str] = Field(
        default=None, description="Optional title for the flow chart"
    )


class FlowChartGeneratorTool(ResilientBaseTool):
    """
    LangChain-compatible tool for generating flow charts using Graphviz
    """

    name: str = "flow_chart_generator"
    description: str = (
        "Generate a flow chart using Graphviz. "
        "Provide nodes and their connections. "
        "Example:\n"
        "nodes: {"
        "  'Start': {'style': {'shape': 'oval', 'color': 'lightgreen'}},"
        "  'Decision': {'style': {'shape': 'diamond', 'color': 'lightyellow'}}"
        "}\n"
        "connections: ["
        "  {'from': 'Start', 'to': 'Decision', 'label': 'Begin'},"
        "  {'from': 'Decision', 'to': 'Process', 'label': 'Yes'}"
        "]"
    )
    args_schema: Type[BaseModel] = FlowChartInput
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"
    file_manager_factory: FileManagerFactory

    def _run(
        self,
        nodes: Dict[str, Dict[str, Union[str, Dict[str, str]]]],
        connections: List[Dict[str, str]],
        title: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Synchronous method (not implemented)
        """
        raise NotImplementedError("Call the asynchronous version of the tool")

    async def _arun(
        self,
        nodes: Dict[str, Dict[str, Union[str, Dict[str, str]]]],
        connections: List[Dict[str, str]],
        title: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Asynchronous method to generate a flow chart
        """
        try:
            # Create a Graphviz Digraph for the flow chart
            dot = Digraph(
                "flow_chart",
                filename="flow_chart",
                node_attr={"style": "filled", "color": "lightblue"},
            )

            # Set graph attributes
            dot.attr(rankdir="TB")  # Top to Bottom layout

            # Add title if provided
            if title:
                dot.attr(label=title, labelloc="t", fontsize="16")

            # Determine which nodes are actually used in connections
            connected_nodes: Set[str] = set()
            for connection in connections:
                connected_nodes.add(connection["from"])
                connected_nodes.add(connection["to"])

            # Add only connected nodes with custom styling
            for node_name in connected_nodes:
                # Default style
                node_style = {
                    "shape": "box",
                    "color": "lightblue",
                    "style": "filled",
                    "fontcolor": "black",
                }

                # Update with custom style if provided
                if node_name in nodes and "style" in nodes[node_name]:
                    custom_style = nodes[node_name]["style"]
                    node_style.update(
                        {
                            "shape": custom_style.get("shape", node_style["shape"]),  # type: ignore[union-attr]
                            "color": custom_style.get("color", node_style["color"]),  # type: ignore[union-attr]
                            "style": custom_style.get("style", node_style["style"]),  # type: ignore[union-attr]
                            "fontcolor": custom_style.get(  # type: ignore[union-attr]
                                "font_color", node_style["fontcolor"]
                            ),
                        }
                    )

                # Add node with styling
                dot.node(
                    node_name,
                    node_name,
                    shape=node_style["shape"],
                    color=node_style["color"],
                    style=node_style["style"],
                    fontcolor=node_style["fontcolor"],
                )

            # Add connections
            for connection in connections:
                dot.edge(
                    connection["from"],
                    connection["to"],
                    label=connection.get("label", ""),
                    color=connection.get("color", "black"),
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
                    "FlowChartGeneratorTool: Failed to save image to disk ",
                )
            # Generate URL for the image
            url: Optional[str] = UrlParser.get_url_for_file_name(image_file_name)
            if url is None:
                return (
                    "Failed to save image to disk",
                    "FlowChartGeneratorTool: Failed to save image to disk",
                )
            # Return the image bytes and a description
            artifact: str = f"FlowChartGeneratorTool: Generated flow chart  <{url}> "
            return url, artifact

        except Exception as e:
            logger.error(f"Failed to generate flow chart: {str(e)}")
            raise ValueError(f"Failed to generate flow chart: {str(e)}")
