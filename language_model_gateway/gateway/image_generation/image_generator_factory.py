from typing import Literal

from language_model_gateway.gateway.aws.aws_client_factory import AwsClientFactory
from language_model_gateway.gateway.image_generation.image_generator import (
    ImageGenerator,
)
from language_model_gateway.gateway.image_generation.aws_image_generator import (
    AwsImageGenerator,
)
from language_model_gateway.gateway.image_generation.openai_image_generator import (
    OpenAIImageGenerator,
)


class ImageGeneratorFactory:
    def __init__(self, *, aws_client_factory: AwsClientFactory) -> None:
        self.aws_client_factory = aws_client_factory
        assert self.aws_client_factory is not None
        assert isinstance(self.aws_client_factory, AwsClientFactory)

    # noinspection PyMethodMayBeStatic
    def get_image_generator(
        self, *, model_name: Literal["aws", "openai"]
    ) -> ImageGenerator:
        match model_name:
            case "aws":
                return AwsImageGenerator(aws_client_factory=self.aws_client_factory)
            case "openai":
                return OpenAIImageGenerator()
            case _:
                raise ValueError(f"Unsupported model_name: {model_name}")
