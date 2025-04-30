import logging
import traceback
from datetime import datetime
from enum import Enum
from typing import Annotated, TypedDict, List, Sequence, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, params
from starlette.requests import Request
from starlette.responses import JSONResponse

from language_model_gateway.configs.config_reader.config_reader import ConfigReader
from language_model_gateway.gateway.api_container import get_config_reader

# MCP SDK minimal import
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)


class ErrorDetail(TypedDict):
    message: str
    timestamp: str
    trace_id: str
    call_stack: str


class MCPServerRouter:
    """
    Router class for Model Configuration Provider (MCP) endpoints
    """

    def __init__(
        self,
        prefix: str = "/mcp/v1",
        tags: list[str | Enum] | None = None,
        dependencies: Sequence[params.Depends] | None = None,
    ) -> None:
        """
        Initialize MCP Server Router

        :param prefix: URL prefix for the router
        :param tags: Optional tags for the router
        :param dependencies: Optional dependencies for the router
        """
        self.prefix = prefix
        self.tags = tags or ["mcp"]
        self.dependencies = dependencies or []
        self.router = APIRouter(
            prefix=self.prefix, tags=self.tags, dependencies=self.dependencies
        )
        self._register_routes()

    def _register_routes(self) -> None:
        """Register all routes for this router"""
        self.router.add_api_route(
            "/configs",
            self.get_model_configs,
            methods=["GET"],
            response_model=None,
            summary="Retrieve model configurations",
            description="Retrieves all available model configurations",
            response_description="List of model configurations",
            status_code=200,
        )

        self.router.add_api_route(
            "/mount-sse",
            self.mount_mcp_sse,
            methods=["POST", "GET"],
            response_model=None,
            summary="Mount MCP Server-Sent Events",
            description="Mounts the MCP server as a Server-Sent Events endpoint",
            response_description="MCP SSE mounting status",
            status_code=200,
        )

    async def get_model_configs(
        self,
        request: Request,
        config_reader: Annotated[ConfigReader, Depends(get_config_reader)],
    ) -> JSONResponse:
        """
        Retrieve model configurations

        :param request: The incoming request
        :param config_reader: Injected configuration reader
        :return: JSON response with model configurations
        :raises HTTPException: For various error conditions
        """
        try:
            configs = await config_reader.read_model_configs_async()
            return JSONResponse(content=[config.model_dump() for config in configs])
        except Exception as e:
            call_stack = traceback.format_exc()
            error_detail: ErrorDetail = {
                "message": "Failed to retrieve model configurations",
                "timestamp": datetime.now().isoformat(),
                "trace_id": "",
                "call_stack": call_stack,
            }
            logger.exception(e, stack_info=True)
            raise HTTPException(status_code=500, detail=error_detail)

    async def mount_mcp_sse(
        self,
        request: Request,
        config_reader: Annotated[ConfigReader, Depends(get_config_reader)],
    ) -> JSONResponse:
        """
        Mount MCP server as Server-Sent Events

        :param request: The incoming request
        :param config_reader: Injected configuration reader
        :return: JSON response with mounting status
        :raises HTTPException: For various error conditions
        """
        try:
            # Create MCP server
            mcp = FastMCP("Model Configuration Gateway")

            @mcp.resource("configs://all")
            async def get_all_configs() -> List[Dict[str, Any]]:
                """Retrieve all model configurations"""
                configs = await config_reader.read_model_configs_async()
                return [config.model_dump() for config in configs]

            @mcp.resource("config://{model_name}")
            async def get_model_config(model_name: str) -> Dict[str, Any]:
                """Retrieve configuration for a specific model"""
                configs = await config_reader.read_model_configs_async()
                for config in configs:
                    if config.name == model_name:
                        return config.model_dump()
                raise HTTPException(
                    status_code=404, detail=f"Model {model_name} not found"
                )

            @mcp.tool()
            async def refresh_configs() -> str:
                """Refresh model configurations"""
                await config_reader.clear_cache()
                configs = await config_reader.read_model_configs_async()
                return f"Refreshed {len(configs)} configurations"

            # Optionally mount the SSE endpoint
            # Note: Actual mounting would typically be done at the app level
            return JSONResponse(
                content={
                    "status": "success",
                    "message": "MCP SSE server created successfully",
                    "resources": ["configs://all", "config://{model_name}"],
                    "timestamp": datetime.now().isoformat(),
                }
            )

        except Exception as e:
            call_stack = traceback.format_exc()
            error_detail: ErrorDetail = {
                "message": "Failed to create MCP SSE server",
                "timestamp": datetime.now().isoformat(),
                "trace_id": "",
                "call_stack": call_stack,
            }
            logger.exception(e, stack_info=True)
            raise HTTPException(status_code=500, detail=error_detail)

    def get_router(self) -> APIRouter:
        """
        Get the configured router

        :return: Configured APIRouter
        """
        return self.router
