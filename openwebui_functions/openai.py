"""title: LangChain Pipe Function (Streaming Version)
author: Colby Sawyer @ Attollo LLC (mailto:colby.sawyer@attollodefense.com)
author_url: https://github.com/ColbySawyer7
version: 0.2.0
This module defines a Pipe class that utilizes LangChain with streaming support
"""

import asyncio
import time
from typing import AsyncGenerator
from typing import Optional, Callable, Awaitable, Any, Dict, Union

from pydantic import BaseModel, Field
from starlette.requests import Request
from starlette.responses import StreamingResponse


class Pipe:
    class Valves(BaseModel):
        emit_interval: float = Field(
            default=2.0, description="Interval in seconds between status emissions"
        )
        enable_status_indicator: bool = Field(
            default=True, description="Enable or disable status indicator emissions"
        )

    def __init__(self) -> None:
        self.type: str = "pipe"
        self.id: str = "langchain_pipe"
        self.name: str = "LangChain Pipe"
        self.valves = self.Valves()
        self.last_emit_time: float = 0

    async def emit_status(
        self,
        __event_emitter__: Optional[Callable[[Dict[str, Any]], Awaitable[None]]],
        level: str,
        message: str,
        done: bool,
    ) -> None:
        current_time = time.time()
        if (
            __event_emitter__
            and self.valves.enable_status_indicator
            and (
                current_time - self.last_emit_time >= self.valves.emit_interval or done
            )
        ):
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "status": "complete" if done else "in_progress",
                        "level": level,
                        "description": message,
                        "done": done,
                    },
                }
            )
            self.last_emit_time = current_time

    async def stream_response(
        self,
        *,
        body: Dict[str, Any],
        __request__: Optional[Request] = None,
        __user__: Optional[Dict[str, Any]] = None,
        __event_emitter__: Callable[[Dict[str, Any]], Awaitable[None]] | None = None,
        __event_call__: Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]
        | None = None,
    ) -> AsyncGenerator[str, None]:
        """
        Async generator to stream response chunks
        """
        try:
            await self.emit_status(
                __event_emitter__,
                "info",
                f"/initiating Chain: {__request__=} {__user__=} {body=}",
                False,
            )

            if __request__ is None or __user__ is None:
                raise ValueError("Request and user information must be provided.")

            # Simulate streaming response
            chunks = [
                f"Headers: {__request__.headers}\n",
                f"Cookies: {__request__.cookies}\n",
                f"User: {__user__}\n",
                f"Body: {body}\n",
            ]

            for chunk in chunks:
                yield chunk
                await self.emit_status(__event_emitter__, "info", "Streaming...", False)
                await asyncio.sleep(0.5)  # Simulate streaming delay

            await self.emit_status(__event_emitter__, "info", "Stream Complete", True)

        except Exception as e:
            error_msg = f"Error: {e}"
            yield error_msg
            await self.emit_status(__event_emitter__, "error", error_msg, True)

    async def pipe(
        self,
        body: Dict[str, Any],
        __request__: Optional[Request] = None,
        __user__: Optional[Dict[str, Any]] = None,
        __event_emitter__: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None,
        __event_call__: Optional[
            Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]
        ] = None,
    ) -> Union[Dict[str, Any], StreamingResponse]:
        """
        Main pipe method supporting both streaming and non-streaming responses
        """
        try:
            # Return a streaming response
            return StreamingResponse(
                self.stream_response(
                    body=body,
                    __request__=__request__,
                    __user__=__user__,
                    __event_emitter__=__event_emitter__,
                    __event_call__=__event_call__,
                ),
                media_type="text/plain",
            )

        except Exception as e:
            await self.emit_status(__event_emitter__, "error", str(e), True)
            return {
                "id": "error",
                "model": "error",
                "created": "2023-10-01T00:00:00Z",
                "choices": [
                    {
                        "index": "1",
                        "message": {
                            "role": "assistant",
                            "content": f"Error: {e}",
                        },
                    }
                ],
            }
