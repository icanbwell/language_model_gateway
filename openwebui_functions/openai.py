"""title: LangChain Pipe Function (Streaming Version)
author: Colby Sawyer @ Attollo LLC (mailto:colby.sawyer@attollodefense.com)
author_url: https://github.com/ColbySawyer7
version: 0.2.0
This module defines a Pipe class that utilizes LangChain with streaming support
"""

import asyncio
import json
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
            # Generate chunks in OpenAI streaming format
            chunks = [
                {
                    "id": "chatcmpl-123",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": "gpt-3.5-turbo",
                    "choices": [
                        {
                            "index": 0,
                            "delta": {"role": "assistant"},
                            "finish_reason": None,
                        }
                    ],
                },
                {
                    "id": "chatcmpl-123",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": "gpt-3.5-turbo",
                    "choices": [
                        {
                            "index": 0,
                            "delta": {"content": "Here"},
                            "finish_reason": None,
                        }
                    ],
                },
                {
                    "id": "chatcmpl-123",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": "gpt-3.5-turbo",
                    "choices": [
                        {"index": 0, "delta": {"content": " is"}, "finish_reason": None}
                    ],
                },
                {
                    "id": "chatcmpl-123",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": "gpt-3.5-turbo",
                    "choices": [
                        {"index": 0, "delta": {"content": " a"}, "finish_reason": None}
                    ],
                },
                {
                    "id": "chatcmpl-123",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": "gpt-3.5-turbo",
                    "choices": [
                        {
                            "index": 0,
                            "delta": {"content": " streamed"},
                            "finish_reason": None,
                        }
                    ],
                },
                {
                    "id": "chatcmpl-123",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": "gpt-3.5-turbo",
                    "choices": [
                        {
                            "index": 0,
                            "delta": {
                                "content": f", headers={__request__.headers}, cookies={__request__.cookies} {__user__=} {body=}",
                            },
                            "finish_reason": None,
                        }
                    ],
                },
                {
                    "id": "chatcmpl-123",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": "gpt-3.5-turbo",
                    "choices": [
                        {
                            "index": 0,
                            "delta": {"content": " response."},
                            "finish_reason": None,
                        }
                    ],
                },
                {
                    "id": "chatcmpl-123",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": "gpt-3.5-turbo",
                    "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
                },
            ]

            for chunk in chunks:
                # Yield each chunk as a JSON-encoded string with a data: prefix
                yield f"data: {json.dumps(chunk)}\n\n"
                await self.emit_status(__event_emitter__, "info", "Streaming...", False)
                await asyncio.sleep(0.5)  # Simulate streaming delay

            await self.emit_status(__event_emitter__, "info", "Stream Complete", True)

        except Exception as e:
            error_chunk = {
                "id": "chatcmpl-error",
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": "error",
                "choices": [
                    {
                        "index": 0,
                        "delta": {"content": f"Error: {str(e)}"},
                        "finish_reason": "stop",
                    }
                ],
            }
            yield f"data: {json.dumps(error_chunk)}\n\n"
            await self.emit_status(__event_emitter__, "error", str(e), True)

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
