"""
title: LangChain Pipe Function
author: Colby Sawyer @ Attollo LLC (mailto:colby.sawyer@attollodefense.com)
author_url: https://github.com/ColbySawyer7
version: 0.1.0

This module defines a Pipe class that utilizes LangChain
"""
import time
from typing import Optional, Callable, Awaitable

from open_webui.models.users import Users
from open_webui.utils.chat import generate_chat_completion
from pydantic import BaseModel, Field


class Pipe:
    class Valves(BaseModel):
        emit_interval: float = Field(
            default=2.0, description="Interval in seconds between status emissions"
        )
        enable_status_indicator: bool = Field(
            default=True, description="Enable or disable status indicator emissions"
        )

    def __init__(self):
        self.type = "pipe"
        self.id = "langchain_pipe"
        self.name = "LangChain Pipe"
        self.valves = self.Valves()
        self.last_emit_time = 0
        pass

    async def emit_status(
            self,
            __event_emitter__: Callable[[dict], Awaitable[None]],
            level: str,
            message: str,
            done: bool,
    ):
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

    async def pipe(
            self, body: dict,
            __request__: Optional[dict] = None,
            __user__: Optional[dict] = None,
            __event_emitter__: Callable[[dict], Awaitable[None]] = None,
            __event_call__: Callable[[dict], Awaitable[dict]] = None,
    ) -> Optional[dict]:
        try:
            await self.emit_status(
                __event_emitter__, "info", "/initiating Chain", False
            )
            messages = body.get("messages", [])
            user = None
            if __user__ is not None:
                # Use the unified endpoint with the updated signature
                user = Users.get_user_by_id(__user__["id"])
            await self.emit_status(
                __event_emitter__, "info", "Starting Chain", False
            )
            messages = body.get("messages", [])
            # Verify a message is available
            if messages:
                question = messages[-1]["content"]
            # If no message is available alert user
            else:
                await self.emit_status(__event_emitter__, "error", "No messages found in the request body", True)
                body["messages"].append({"role": "assistant", "content": "No messages found in the request body"})

            await self.emit_status(__event_emitter__, "info", "Complete", True)

            return await generate_chat_completion(__request__, body, user)
        except Exception as e:
            await self.emit_status(__event_emitter__, "error", str(e), True)
            formatted_response = {
                "id": "error",
                "model": "error",
                "created": "2023-10-01T00:00:00Z",
                # "usage": response["usage"],
                # "object": response["object"],
                "choices": [
                    {
                        "index": "1",
                        # "finish_reason": choice["finish_reason"],
                        "message": {
                            "role": "assistant",
                            "content": f"Error: {e}",
                        },
                        # "delta": {"role": "assistant", "content": ""},
                    }
                ],
            }
            return formatted_response
