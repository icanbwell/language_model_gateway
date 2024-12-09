import asyncio
import logging
import os
from typing import List, Optional
from urllib.parse import urlparse, ParseResult
from uuid import UUID, uuid4

from language_model_gateway.configs.config_reader.file_config_reader import (
    FileConfigReader,
)
from language_model_gateway.configs.config_reader.github_config_reader import (
    GitHubConfigReader,
)
from language_model_gateway.configs.config_reader.s3_config_reader import S3ConfigReader
from language_model_gateway.configs.config_schema import ChatModelConfig
from language_model_gateway.gateway.utilities.expiring_cache import ExpiringCache


logger = logging.getLogger(__name__)


class ConfigReader:
    _identifier: UUID = uuid4()
    _lock: asyncio.Lock = asyncio.Lock()

    def __init__(self, *, cache: ExpiringCache[List[ChatModelConfig]]) -> None:
        """
        Initialize the async config reader

        Args:
            cache: Expiring cache for model configurations
        """
        assert cache is not None
        self._cache: ExpiringCache[List[ChatModelConfig]] = cache
        assert self._cache is not None

    # noinspection PyMethodMayBeStatic
    async def read_model_configs_async(self) -> List[ChatModelConfig]:
        config_path: str = os.environ["CONFIG_PATH"]
        assert config_path is not None, "CONFIG_PATH environment variable is not set"

        # Check cache first
        cached_configs: List[ChatModelConfig] | None = await self._cache.get()
        if cached_configs is not None:
            logger.debug(
                f"ConfigReader with id: {self._identifier} using cached model configurations"
            )
            return cached_configs
        else:
            logger.info(f"ConfigReader with id: {self._identifier} cache is empty")

        # Use lock to prevent multiple simultaneous loads
        async with self._lock:
            # Check again in case another request loaded the configs while we were waiting
            cached_configs = await self._cache.get()
            if cached_configs is not None:
                logger.debug(
                    f"ConfigReader with id: {self._identifier} using cached model configurations"
                )
                return cached_configs

            logger.info(
                f"ConfigReader with id: {self._identifier} reading model configurations from {config_path}"
            )

            def is_github_url(url: str) -> bool:
                parsed_url: ParseResult = urlparse(url)
                host: Optional[str] = parsed_url.hostname
                return host is not None and (
                    host == "github.com" or host.endswith(".github.com")
                )

            models: List[ChatModelConfig]
            if config_path.startswith("s3"):
                models = await S3ConfigReader().read_model_configs(s3_url=config_path)
                logger.info(
                    f"ConfigReader with id:  {self._identifier} loaded {len(models)} model configurations from S3"
                )
            elif is_github_url(config_path):
                models = await GitHubConfigReader().read_model_configs(
                    github_url=config_path
                )
                logger.info(
                    f"ConfigReader with id:  {self._identifier} loaded {len(models)} model configurations from GitHub"
                )
            else:
                models = FileConfigReader().read_model_configs(config_path=config_path)
                logger.info(
                    f"ConfigReader with id:  {self._identifier} loaded {len(models)} model configurations from file system"
                )

            # if we can't load models another way then try to load them from the file system
            if not models or len(models) == 0:
                config_path_backup: str = os.environ["CONFIG_PATH_BACKUP"]
                models = FileConfigReader().read_model_configs(
                    config_path=config_path_backup
                )
                logger.info(
                    f"ConfigReader with id:  {self._identifier} loaded {len(models)} model configurations from backup config store"
                )

            # remove any models that are marked disabled
            models = [model for model in models if not model.disabled]
            await self._cache.set(models)
            return models

    async def clear_cache(self) -> None:
        await self._cache.clear()
        logger.info(f"ConfigReader with id:  {self._identifier} cleared cache")