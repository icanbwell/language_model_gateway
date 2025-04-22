import logging
import os
import tempfile
from typing import Type, Literal, Tuple, Optional, List, Dict, Union, Any
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


class ERDiagramInput(BaseModel):
    """
    Input model for Entity-Relationship Diagram generation

    Example input:
    {
        "entities": {
            "User": {
                "attributes": [
                    {"name": "id", "primary": True},
                    {"name": "username", "primary": False},
                    {"name": "email", "primary": False}
                ],
                "style": {"color": "lightblue"}
            },
            "Order": {
                "attributes": [
                    {"name": "order_id", "primary": True},
                    {"name": "user_id", "primary": False},
                    {"name": "total", "primary": False}
                ],
                "style": {"color": "lightgreen"}
            }
        },
        "relationships": [
            {
                "from": "User",
                "to": "Order",
                "label": "places",
                "cardinality": "one_to_many"
            }
        ],
        "title": "User Order System"
    }
    """

    entities: Dict[str, Dict[str, Union[List[Dict[str, Any]], Dict[str, str]]]] = Field(
        description="Dictionary of entities with their attributes and optional styling"
    )
    relationships: List[Dict[str, str]] = Field(
        description="List of relationships between entities"
    )
    title: Optional[str] = Field(
        default=None, description="Optional title for the ER diagram"
    )


class ERDiagramGeneratorTool(ResilientBaseTool):
    """
    LangChain-compatible tool for generating Entity-Relationship Diagrams using Graphviz
    """

    name: str = "er_diagram_generator"
    description: str = (
        "Generate an Entity-Relationship Diagram using Graphviz. "
        "Provide entities with attributes and their relationships. "
        "Example:\n"
        "entities: {"
        "  'User': {"
        "    'attributes': ["
        "      {'name': 'id', 'primary': True},"
        "      {'name': 'username', 'primary': False}"
        "    ]"
        "  }"
        "}\n"
        "relationships: ["
        "  {'from': 'User', 'to': 'Order', 'label': 'places'}"
        "]"
    )
    args_schema: Type[BaseModel] = ERDiagramInput
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"
    file_manager_factory: FileManagerFactory

    def _run(
        self,
        entities: Dict[str, Dict[str, Union[List[Dict[str, Any]], Dict[str, str]]]],
        relationships: List[Dict[str, str]],
        title: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Synchronous method (not implemented)
        """
        raise NotImplementedError("Call the asynchronous version of the tool")

    async def _arun(
        self,
        entities: Dict[str, Dict[str, Union[List[Dict[str, Any]], Dict[str, str]]]],
        relationships: List[Dict[str, str]],
        title: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Asynchronous method to generate an ER Diagram
        """
        try:
            # Create a Graphviz Digraph for the ER diagram
            dot = Digraph(
                "er_diagram",
                filename="er_diagram",
                node_attr={"style": "filled", "color": "lightblue"},
            )

            # Set graph attributes
            dot.attr(rankdir="TB")  # Top to Bottom layout

            # Add title if provided
            if title:
                dot.attr(label=title, labelloc="t", fontsize="16")

            # Cardinality and relationship line styles
            cardinality_styles = {
                "one_to_many": "crow",
                "one_to_one": "none",
                "many_to_many": "crow",
            }

            # Add entities with attributes
            for entity_name, entity_details in entities.items():
                # Prepare entity label with attributes
                label_parts = [entity_name]

                # Add attributes
                if "attributes" in entity_details:
                    attributes = entity_details["attributes"]
                    attribute_lines = []
                    for attr in attributes:
                        attr_name = attr["name"]  # type: ignore[index]
                        # Mark primary key with *
                        attr_display = (
                            f"{'*' if attr.get('primary', False) else ''}{attr_name}"  # type: ignore[union-attr]
                        )
                        attribute_lines.append(attr_display)

                    # Combine attributes into label
                    if attribute_lines:
                        label_parts.append("|" + "\\l".join(attribute_lines) + "\\l")

                # Create node with record shape
                node_style = {
                    "shape": "record",
                    "color": entity_details.get("style", {}).get("color", "lightblue"),  # type: ignore[union-attr]
                    "style": "filled",
                }

                dot.node(
                    entity_name,
                    "".join(label_parts),
                    shape=node_style["shape"],
                    color=node_style["color"],
                    style=node_style["style"],
                )

            # Add relationships
            for relationship in relationships:
                dot.edge(
                    relationship["from"],
                    relationship["to"],
                    label=relationship.get("label", ""),
                    arrowhead=cardinality_styles.get(
                        relationship.get("cardinality", "one_to_many"), "none"
                    ),
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
                    "ERDiagramGeneratorTool: Failed to save image to disk ",
                )

            # Generate URL for the image
            url: Optional[str] = UrlParser.get_url_for_file_name(image_file_name)

            if url is None:
                return (
                    "Failed to save image to disk",
                    "ERDiagramGeneratorTool: Failed to save image to disk",
                )

            artifact: str = f"ERDiagramGeneratorTool: Generated ER diagram with {len(entities)} entities <{url}> "
            # Return the image bytes and a description
            return url, artifact

        except Exception as e:
            logger.error(f"Failed to generate ER diagram: {str(e)}")
            raise ValueError(f"Failed to generate ER diagram: {str(e)}")
