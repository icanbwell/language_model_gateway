import logging
import time
from typing import Dict, List, Any

from openai.types import Model

from language_model_gateway.configs.config_reader.config_reader import ConfigReader
from language_model_gateway.configs.config_schema import ChatModelConfig


class ModelManager:
    def __init__(self, *, config_reader: ConfigReader) -> None:
        self.config_reader: ConfigReader = config_reader
        assert self.config_reader is not None
        assert isinstance(self.config_reader, ConfigReader)

    # noinspection PyMethodMayBeStatic
    async def get_models(
        self,
        *,
        headers: Dict[str, str],
    ) -> Dict[str, str | List[Dict[str, str | int]]]:
        configs: List[
            ChatModelConfig
        ] = await self.config_reader.read_model_configs_async()
        logger = logging.getLogger(__name__)
        logger.info("Received request for models")
        # get time in seconds since epoch from ten minutes ago

        models: List[Model] = [
            Model(
                id=config.name,
                created=int(time.time()),
                object="model",
                owned_by="openai",
            )
            for config in configs
        ]
        models_list: List[Dict[str, Any]] = [model.model_dump() for model in models]
        # return {"data": models_list}
        # models2 = [
        #     {"id": config.name, "description": config.description, "created": 1686935002} for config in configs
        # ]
        return {"object": "list", "data": models_list}
