import logging
from typing import Annotated

from fastapi import Depends

from language_model_gateway.configs.config_reader.config_reader import ConfigReader
from language_model_gateway.container.container_factory import ContainerFactory
from language_model_gateway.container.simple_container import SimpleContainer
from language_model_gateway.gateway.aws.aws_client_factory import AwsClientFactory
from language_model_gateway.gateway.file_managers.file_manager_factory import (
    FileManagerFactory,
)
from language_model_gateway.gateway.managers.chat_completion_manager import (
    ChatCompletionManager,
)
from language_model_gateway.gateway.managers.image_generation_manager import (
    ImageGenerationManager,
)
from language_model_gateway.gateway.managers.model_manager import ModelManager
from language_model_gateway.gateway.utilities.cached import cached
from language_model_gateway.gateway.utilities.tokens.well_known_configuration_reader.well_known_configuration_reader import (
    WellKnownConfigurationReader,
)

logger = logging.getLogger(__name__)


@cached  # makes it singleton-like
async def get_container_async() -> SimpleContainer:
    """Create the container"""
    return await ContainerFactory().create_container_async()


def get_chat_manager(
    container: Annotated[SimpleContainer, Depends(get_container_async)],
) -> ChatCompletionManager:
    """helper function to get the chat manager"""
    assert isinstance(container, SimpleContainer), type(container)
    return container.resolve(ChatCompletionManager)


def get_model_manager(
    container: Annotated[SimpleContainer, Depends(get_container_async)],
) -> ModelManager:
    """helper function to get the model manager"""
    assert isinstance(container, SimpleContainer), type(container)
    return container.resolve(ModelManager)


def get_image_generation_manager(
    container: Annotated[SimpleContainer, Depends(get_container_async)],
) -> ImageGenerationManager:
    """helper function to get the model manager"""
    assert isinstance(container, SimpleContainer), type(container)
    return container.resolve(ImageGenerationManager)


def get_config_reader(
    container: Annotated[SimpleContainer, Depends(get_container_async)],
) -> ConfigReader:
    """helper function to get the chat manager"""
    assert isinstance(container, SimpleContainer), type(container)
    return container.resolve(ConfigReader)


def get_aws_client_factory(
    container: Annotated[SimpleContainer, Depends(get_container_async)],
) -> AwsClientFactory:
    """helper function to get the chat manager"""
    assert isinstance(container, SimpleContainer), type(container)
    return container.resolve(AwsClientFactory)


def get_file_manager_factory(
    container: Annotated[SimpleContainer, Depends(get_container_async)],
) -> FileManagerFactory:
    """helper function to get the chat manager"""
    assert isinstance(container, SimpleContainer), type(container)
    return container.resolve(FileManagerFactory)


def get_well_known_configuration_reader(
    container: Annotated[SimpleContainer, Depends(get_container_async)],
) -> WellKnownConfigurationReader:
    """helper function to get the chat manager"""
    assert isinstance(container, SimpleContainer), type(container)
    return container.resolve(WellKnownConfigurationReader)
