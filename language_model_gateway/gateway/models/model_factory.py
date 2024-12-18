import logging
import os
from typing import List, Any, Dict

from langchain_aws import ChatBedrockConverse
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from language_model_gateway.configs.config_schema import (
    ModelConfig,
    ModelParameterConfig,
    ChatModelConfig,
)

logger = logging.getLogger(__name__)


class ModelFactory:
    # noinspection PyMethodMayBeStatic
    def get_model(self, chat_model_config: ChatModelConfig) -> BaseChatModel:
        assert chat_model_config is not None
        assert isinstance(chat_model_config, ChatModelConfig)
        model_config: ModelConfig | None = chat_model_config.model
        if model_config is None:
            # if no model configuration is provided, use the default model
            default_model_provider: str = os.environ.get(
                "DEFAULT_MODEL_PROVIDER", "bedrock"
            )
            default_model_name: str = os.environ.get(
                "DEFAULT_MODEL_NAME", "us.anthropic.claude-3-5-haiku-20241022-v1:0"
            )
            model_config = ModelConfig(
                provider=default_model_provider, model=default_model_name
            )

        model_vendor: str = model_config.provider
        model_name: str = model_config.model

        model_parameters: List[ModelParameterConfig] | None = (
            chat_model_config.model_parameters
        )

        # convert model_parameters to dict
        model_parameters_dict: Dict[str, Any] = {}
        if model_parameters is not None:
            model_parameter: ModelParameterConfig
            for model_parameter in model_parameters:
                model_parameters_dict[model_parameter.key] = model_parameter.value

        logger.debug(f"Creating ChatModel with parameters: {model_parameters_dict}")
        model_parameters_dict["model"] = model_name
        # model_parameters_dict["streaming"] = True
        llm: BaseChatModel
        if model_vendor == "openai":
            llm = ChatOpenAI(**model_parameters_dict)
        elif model_config.provider == "bedrock":
            llm = ChatBedrockConverse(
                client=None,
                provider="anthropic",
                credentials_profile_name=os.environ.get("AWS_CREDENTIALS_PROFILE"),
                region_name=os.environ.get("AWS_REGION", "us-east-1"),
                # Setting temperature to 0 for deterministic results
                **model_parameters_dict,
            )
        elif model_config.provider == "openai":
            llm = ChatOpenAI(**model_parameters_dict)
        else:
            raise ValueError(
                f"Unsupported model vendor: {model_vendor} and model_provider: {model_config.provider} for {model_name}"
            )

        return llm
