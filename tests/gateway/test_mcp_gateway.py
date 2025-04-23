import httpx
import pytest
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream

from mcp.client.websocket import websocket_client
from mcp.client.sse import sse_client
from mcp.types import JSONRPCMessage
from mcp import ClientSession, ReadResourceResult
from pydantic import AnyUrl


@pytest.mark.asyncio
async def test_mcp_configs_via_websocket(async_client: httpx.AsyncClient) -> None:
    """
    Test retrieving model configurations using MCP websocket client
    """
    print("Testing MCP Configurations Retrieval via websocket client")

    read: MemoryObjectReceiveStream[JSONRPCMessage | Exception]
    write: MemoryObjectSendStream[JSONRPCMessage]
    # Use websocket client
    async with websocket_client("ws://localhost:5000/mcp/v1") as (read, write):
        async with ClientSession(read, write) as session:
            # Retrieve all configs
            configs: ReadResourceResult = await session.read_resource(
                uri=AnyUrl("configs://all")
            )

            # Validate response
            assert isinstance(configs, list), "Configs should be a list"
            assert len(configs) > 0, "At least one configuration should be returned"

            # Check basic configuration structure
            for config in configs:
                assert "model_name" in config, f"Missing model_name in config: {config}"
                assert isinstance(config, dict), "Each config should be a dictionary"


@pytest.mark.asyncio
async def test_mcp_configs_via_sse(async_client: httpx.AsyncClient) -> None:
    """
    Test retrieving model configurations using MCP SSE client
    """
    print("Testing MCP Configurations Retrieval via SSE client")

    # Use SSE client
    async with sse_client("http://localhost:5000/mcp/v1") as mcp_client:
        # Retrieve all configs
        configs = await mcp_client.resource("configs://all").get()

        # Validate response
        assert isinstance(configs, list), "Configs should be a list"
        assert len(configs) > 0, "At least one configuration should be returned"

        # Check basic configuration structure
        for config in configs:
            assert "model_name" in config, f"Missing model_name in config: {config}"
            assert isinstance(config, dict), "Each config should be a dictionary"
