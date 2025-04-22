import logging
import os
import tempfile
from typing import Type, Literal, Tuple, Optional, List, Dict, Any
from uuid import uuid4

from graphviz import Graph  # Note: Using Graph instead of Digraph
from pydantic import BaseModel, Field

from language_model_gateway.gateway.file_managers.file_manager import FileManager
from language_model_gateway.gateway.file_managers.file_manager_factory import (
    FileManagerFactory,
)
from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool
from language_model_gateway.gateway.utilities.url_parser import UrlParser

logger = logging.getLogger(__name__)


class NetworkTopologyInput(BaseModel):
    """
    Input model for network topology diagram generation

    Example input:
    {
        "nodes": {
            "Internet": {"type": "cloud", "location": "external"},
            "Router": {"type": "router", "location": "edge"},
            "Switch1": {"type": "switch", "location": "distribution"},
            "Server1": {"type": "server", "location": "internal"}
        },
        "connections": [
            {"from": "Internet", "to": "Router", "type": "wan", "bandwidth": "1 Gbps"},
            {"from": "Router", "to": "Switch1", "type": "lan", "bandwidth": "10 Gbps"},
            {"from": "Switch1", "to": "Server1", "type": "access", "bandwidth": "1 Gbps"}
        ],
        "title": "Simple Network Topology"
    }
    """

    nodes: Dict[str, Dict[str, str]] = Field(
        description="Dictionary of network nodes with type and location"
    )
    connections: List[Dict[str, str]] = Field(
        description="List of connections between nodes with details"
    )
    title: Optional[str] = Field(
        default=None, description="Optional title for the network topology diagram"
    )


class NetworkTopologyGeneratorTool(ResilientBaseTool):
    """
    LangChain-compatible tool for generating network topology diagrams
    """

    name: str = "network_topology_generator"
    description: str = "Generate a network topology diagram using Graphviz"

    args_schema: Type[BaseModel] = NetworkTopologyInput
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"
    file_manager_factory: FileManagerFactory

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Use async version of this tool")

    async def _arun(
        self,
        nodes: Dict[str, Dict[str, str]],
        connections: List[Dict[str, str]],
        title: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Asynchronous method to generate a network topology diagram
        """
        try:
            # Create a Graphviz Graph (undirected) for network topology
            dot = Graph(
                "network_topology",
                filename="network_topology",
                engine="neato",  # Use neato for more spread-out layout
                strict=True,  # Prevent multiple edges between same nodes
            )

            # Set graph attributes for a more network-like layout
            dot.attr(
                overlap="false",  # Prevent node overlapping
                splines="true",  # Use curved edges
                sep="0.5",  # Add spacing between nodes
            )

            # Add title if provided
            if title:
                dot.attr(label=title, labelloc="t", fontsize="16")

            # Node type to shape and color mapping
            node_styles = {
                "cloud": {
                    "shape": "ellipse",
                    "style": "filled",
                    "color": "lightgray",
                    "fontcolor": "black",
                },
                "router": {
                    "shape": "diamond",
                    "style": "filled",
                    "color": "lightblue",
                    "fontcolor": "black",
                },
                "switch": {
                    "shape": "box",
                    "style": "filled",
                    "color": "lightgreen",
                    "fontcolor": "black",
                },
                "server": {
                    "shape": "box3d",
                    "style": "filled",
                    "color": "lightcoral",
                    "fontcolor": "black",
                },
                "firewall": {
                    "shape": "hexagon",
                    "style": "filled",
                    "color": "lightsalmon",
                    "fontcolor": "black",
                },
                "default": {
                    "shape": "circle",
                    "style": "filled",
                    "color": "lightblue",
                    "fontcolor": "black",
                },
            }

            # Connection type to style mapping
            connection_styles = {
                "wan": {"style": "dashed", "color": "red"},
                "lan": {"style": "solid", "color": "green"},
                "access": {"style": "dotted", "color": "blue"},
                "default": {"style": "solid", "color": "black"},
            }

            # Add nodes with custom styling
            for node_name, node_details in nodes.items():
                # Determine node style based on type
                node_type = node_details.get("type", "default").lower()
                node_style = node_styles.get(node_type, node_styles["default"])

                # Add node with detailed styling
                dot.node(
                    node_name,
                    node_name,
                    shape=node_style["shape"],
                    style=node_style["style"],
                    color=node_style["color"],
                    fontcolor=node_style["fontcolor"],
                )

            # Add connections with custom styling
            for connection in connections:
                # Determine connection style
                conn_type = connection.get("type", "default").lower()
                conn_style = connection_styles.get(
                    conn_type, connection_styles["default"]
                )

                # Create edge with style and optional label
                dot.edge(
                    connection["from"],
                    connection["to"],
                    style=conn_style["style"],
                    color=conn_style["color"],
                    label=connection.get("bandwidth", ""),
                )

            # Render the diagram to bytes
            image_data: bytes = dot.pipe(format="png")

            # Generate a unique filename
            image_file_name: str = f"{uuid4()}.png"

            # Use file manager to save the file
            image_generation_path_ = os.environ.get(
                "IMAGE_GENERATION_PATH", tempfile.gettempdir()
            )
            file_manager: FileManager = self.file_manager_factory.get_file_manager(
                folder=image_generation_path_
            )
            file_path: Optional[str] = await file_manager.save_file_async(
                file_data=image_data,
                folder=image_generation_path_,
                filename=image_file_name,
            )
            # Attempt to save the file
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

            artifact: str = f"NetworkTopologyGeneratorTool: Generated network topology diagram <{url}> "
            # Return the image bytes and a description
            return url, artifact

        except Exception as e:
            logger.error(f"Failed to generate network topology diagram: {str(e)}")
            raise ValueError(f"Failed to generate network topology diagram: {str(e)}")
