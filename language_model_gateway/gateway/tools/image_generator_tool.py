import base64
import logging
import os
from typing import Literal, Tuple, Type, Optional
from uuid import uuid4

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from language_model_gateway.gateway.file_managers.file_manager import FileManager
from language_model_gateway.gateway.file_managers.file_manager_factory import (
    FileManagerFactory,
)
from language_model_gateway.gateway.image_generation.image_generator import (
    ImageGenerator,
)
from language_model_gateway.gateway.image_generation.image_generator_factory import (
    ImageGeneratorFactory,
)
from language_model_gateway.gateway.utilities.url_parser import UrlParser

logger = logging.getLogger(__name__)


class ImageGeneratorToolInput(BaseModel):
    prompt: str = Field(description="Prompt to use for generating the image")


class ImageGeneratorTool(BaseTool):
    """
    LangChain-compatible tool for generating an image from a given text.
    """

    name: str = "image_generator"
    description: str = (
        "Generates an image from a given text. "
        "Provide the text as input. "
        # "The tool will return the image as a base64 encoded string in PNG format: `data:image/png;base64,{base64_image}`."
        "The tool will return a url to the generated image."
    )
    args_schema: Type[BaseModel] = ImageGeneratorToolInput
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"
    image_generator_factory: ImageGeneratorFactory
    file_manager_factory: FileManagerFactory
    model_provider: Literal["aws", "openai"]
    image_size: Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"] = (
        "1024x1024"
    )
    style: Literal["natural", "cinematic", "digital-art", "pop-art"] = "natural"
    return_embedded_image: bool = False

    def _run(self, prompt: str) -> Tuple[str, str]:
        """
        Synchronous version of the tool (falls back to async implementation).
        :param prompt: The URL of the webpage to fetch.
        :return: The content of the webpage in Markdown format.
        """
        raise NotImplementedError("Use async version of this tool")

    async def _arun(self, prompt: str) -> Tuple[str, str]:
        """
        Asynchronous version of the tool.
        :param prompt: The URL of the webpage to fetch.
        :return: The content of the webpage in Markdown format.
        """
        try:
            image_generator: ImageGenerator = (
                self.image_generator_factory.get_image_generator(
                    model_name=self.model_provider
                )
            )
            image_data: bytes = await image_generator.generate_image_async(
                prompt=prompt, style=self.style, image_size=self.image_size
            )
            # base64_image: str = base64.b64encode(image_data).decode("utf-8")
            image_generation_path_ = os.environ["IMAGE_GENERATION_PATH"]
            assert (
                image_generation_path_
            ), "IMAGE_GENERATION_PATH environment variable is not set"
            image_file_name: str = f"{uuid4()}.png"
            file_manager: FileManager = self.file_manager_factory.get_file_manager(
                folder=image_generation_path_
            )
            file_path: Optional[str] = await file_manager.save_file_async(
                image_data=image_data,
                folder=image_generation_path_,
                filename=image_file_name,
            )
            if file_path is None:
                return (
                    f"Failed to save image to disk",
                    f"ImageGeneratorTool[{self.model_provider}]: Failed to save image to disk from prompt: {prompt}",
                )

            url: Optional[str] = UrlParser.get_url_for_file_name(image_file_name)
            if url is None:
                return (
                    f"Failed to save image to disk",
                    f"ImageGeneratorTool[{self.model_provider}]: Failed to save image to disk from prompt: {prompt}",
                )

            if self.return_embedded_image:
                base64_image: str = base64.b64encode(image_data).decode("utf-8")
                embedded_url = f"data:image/png;base64,{base64_image}"
                markdown_image = f"![Generated Image]({embedded_url})"
                return (
                    url,
                    f"ImageGeneratorTool[{self.model_provider}]: Generated image from prompt: {prompt}: {markdown_image} ",
                )
            else:
                return (
                    url,
                    f"ImageGeneratorTool[{self.model_provider}]: Generated image from prompt: {prompt}: <{url}> ",
                )
        except Exception as e:
            logger.error(f"Failed to generate image: {str(e)}")
            logger.exception(e, stack_info=True)
            return (
                f"Failed to generate image: {e}",
                f"ImageGeneratorTool[{self.model_provider}]: Failed to generate image from prompt: {prompt}",
            )
