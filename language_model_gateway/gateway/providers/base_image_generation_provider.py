from abc import abstractmethod
from typing import Dict

from starlette.responses import StreamingResponse, JSONResponse

from language_model_gateway.gateway.schema.openai.image_generation import (
    ImageGenerationRequest,
)


class BaseImageGenerationProvider:
    @abstractmethod
    async def generate_image_async(
        self,
        *,
        image_generation_request: ImageGenerationRequest,
        headers: Dict[str, str],
    ) -> StreamingResponse | JSONResponse: ...
