"""
title: LangChain Pipe Function
author: Colby Sawyer @ Attollo LLC (mailto:colby.sawyer@attollodefense.com)
author_url: https://github.com/ColbySawyer7
version: 0.1.0

This module defines a Pipe class that utilizes LangChain
"""

import time
from typing import Optional, Callable, Awaitable, Any, Dict
from typing import AsyncGenerator, Iterator

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
        pass

    async def emit_status(
        self,
        __event_emitter__: Callable[[Dict[str, Any]], Awaitable[None]] | None,
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

    async def pipe(
        self,
        body: Dict[str, Any],
        __request__: Optional[Request] = None,
        __user__: Optional[Dict[str, Any]] = None,
        __event_emitter__: Callable[[Dict[str, Any]], Awaitable[None]] | None = None,
        __event_call__: Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]
        | None = None,
    ) -> (
        Dict[str, Any]
        | StreamingResponse
        | BaseModel
        | Iterator[Dict[str, Any] | BaseModel | str]
        | AsyncGenerator[Dict[str, Any] | BaseModel | str, None]
    ):
        """
        Called from https://github.com/open-webui/open-webui/blob/main/backend/open_webui/functions.py


        """
        try:
            await self.emit_status(
                __event_emitter__,
                "info",
                f"/initiating Chain: {__request__=} {__user__=} {body=}",
                False,
            )
            # user = None
            # await self.emit_status(
            #     __event_emitter__, "info", "Starting Chain", False
            # )
            # result = cast(Dict[str,Any], await generate_chat_completion(__request__, body, user))
            if __request__ is None or __user__ is None:
                raise ValueError("Request and user information must be provided.")
            result: Dict[str, Any] = {
                "id": "chatcmpl-B9MBs8CjcvOU2jLn4n570S5qMJKcT",
                "object": "chat.completion",
                "created": 1741569952,
                "model": "gpt-4.1-2025-04-14",
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": f"headers={__request__.headers}, cookies={__request__.cookies} {__user__=} {body=}",
                            "annotations": [],
                        },
                        "logprobs": None,
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": 19,
                    "completion_tokens": 10,
                    "total_tokens": 29,
                    "prompt_tokens_details": {"cached_tokens": 0, "audio_tokens": 0},
                    "completion_tokens_details": {
                        "reasoning_tokens": 0,
                        "audio_tokens": 0,
                        "accepted_prediction_tokens": 0,
                        "rejected_prediction_tokens": 0,
                    },
                },
                "service_tier": "default",
            }

            await self.emit_status(__event_emitter__, "info", "Complete", True)
            return result
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
