import base64
import logging
import os
from typing import override, Literal, Optional

from openai import AsyncOpenAI
from openai.types import ImagesResponse

from language_model_gateway.gateway.image_generation.image_generator import (
    ImageGenerator,
)


logger = logging.getLogger(__name__)


class OpenAIImageGenerator(ImageGenerator):
    @staticmethod
    async def _invoke_model_async(
        prompt: str,
        image_size: Literal[
            "256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"
        ],
    ) -> bytes:
        """Synchronous OpenAI image generation"""

        openai_api_key: Optional[str] = os.environ.get("OPENAI_API_KEY")
        assert openai_api_key is not None, (
            "OPENAI_API_KEY environment variable is not set"
        )

        client = AsyncOpenAI(api_key=openai_api_key)

        response: ImagesResponse = await client.images.generate(
            model="dall-e-3",  # You can change to "dall-e-2" if needed
            prompt=prompt,
            size=image_size,
            quality="standard",
            n=1,
            response_format="b64_json",
        )

        # Extract the base64 encoded image and decode
        assert response.data is not None and len(response.data) > 0, (
            "Base64 image is None"
        )

        base64_image: Optional[str] = response.data[0].b64_json
        assert base64_image is not None, "Base64 image is None"
        return base64.b64decode(base64_image)

    @override
    async def generate_image_async(
        self,
        *,
        prompt: str,
        style: Literal["natural", "cinematic", "digital-art", "pop-art"] = "natural",
        image_size: Literal[
            "256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"
        ] = "1024x1024",
    ) -> bytes:
        """Generate an image using OpenAI DALL-E"""
        if os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1":
            logger.info(f"Generating image for prompt: {prompt}")

        try:
            # Run model invocation in executor
            image_data: bytes = await self._invoke_model_async(
                prompt=prompt, image_size=image_size
            )

            if os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1":
                logger.info(f"Image generated successfully for prompt: {prompt}")

            return image_data

        except Exception as e:
            logger.error(f"Error generating image for prompt {prompt}: {str(e)}")
            logger.exception(e, stack_info=True)
            raise
