from language_model_gateway.gateway.image_generation.image_generator import (
    ImageGenerator,
)


class ImageGeneratorFactory:
    # noinspection PyMethodMayBeStatic
    def get_image_generator(self, *, model_name: str) -> ImageGenerator:
        match model_name:
            case "aws":
                from language_model_gateway.gateway.image_generation.aws_image_generator import (
                    AwsImageGenerator,
                )

                return AwsImageGenerator()
            case "dall-e-3":
                from language_model_gateway.gateway.image_generation.aws_image_generator import (
                    AwsImageGenerator,
                )

                return AwsImageGenerator()
            case _:
                raise ValueError(f"Unsupported model_name: {model_name}")
