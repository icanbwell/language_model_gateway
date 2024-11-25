import logging
from typing import Dict, Any, cast
from typing import List

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import StreamingResponse, JSONResponse
from language_model_gateway.gateway.managers.chat_completion_manager import (
    ChatCompletionManager,
)
from language_model_gateway.gateway.managers.model_manager import ModelManager
from language_model_gateway.gateway.schema.openai.completions import ChatRequest

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="OpenAI-compatible API")


@app.get("/health")
def health() -> str:
    return "OK"


@app.post("/api/v1/chat/completions", response_model=None)
async def chat_completions(
    request: Request,
    chat_request: Dict[str, Any],
) -> StreamingResponse | JSONResponse:
    return await ChatCompletionManager().chat_completions(
        headers={k: v for k, v in request.headers.items()},
        chat_request=cast(ChatRequest, chat_request),
    )


@app.get("/api/v1/models")
async def get_models() -> Dict[str, List[Dict[str, str]]]:
    return await ModelManager.get_models()
