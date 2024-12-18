from typing import override, Literal

from language_model_gateway.gateway.image_generation.image_generator import (
    ImageGenerator,
)


class MockImageGenerator(ImageGenerator):
    @override
    async def generate_image_async(
        self,
        *,
        prompt: str,
        style: Literal["natural", "cinematic", "digital-art", "pop-art"] = "natural",
        image_size: Literal[
            "256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"
        ] = "1024x1024"
    ) -> bytes:
        return b"mock_image_data"
