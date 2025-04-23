from fastapi import HTTPException, Depends, APIRouter
from language_model_gateway.configs.config_reader.config_reader import ConfigReader
from typing import Annotated, List, Dict, Any
from language_model_gateway.gateway.api_container import get_config_reader


class MCPServerRouter:
    """Router for MCP Server endpoints with dependency injection"""

    def __init__(self) -> None:
        self._router = APIRouter(prefix="/mcp", tags=["Model Configuration Provider"])
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Set up MCP-specific routes"""

        @self._router.get("/configs")
        async def get_model_configs(
            config_reader: Annotated[ConfigReader, Depends(get_config_reader)],
        ) -> List[Dict[str, Any]]:
            """Retrieve all model configurations"""
            configs = await config_reader.read_model_configs_async()
            return [config.model_dump() for config in configs]

        @self._router.get("/config/{model_name}")
        async def get_model_config(
            model_name: str,
            config_reader: Annotated[ConfigReader, Depends(get_config_reader)],
        ) -> Dict[str, Any]:
            """Retrieve configuration for a specific model"""
            configs = await config_reader.read_model_configs_async()
            for config in configs:
                if config.name == model_name:
                    return config.model_dump()
            raise HTTPException(status_code=404, detail=f"Model {model_name} not found")

        @self._router.get("/refresh")
        async def refresh_configs(
            config_reader: Annotated[ConfigReader, Depends(get_config_reader)],
        ) -> Dict[str, Any]:
            """Refresh model configurations"""
            await config_reader.clear_cache()
            configs = await config_reader.read_model_configs_async()
            return {"message": "Configurations refreshed", "count": len(configs)}

    def get_router(self) -> APIRouter:
        """Return the configured router"""
        return self._router
