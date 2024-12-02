from contextlib import asynccontextmanager
from typing import Callable, AsyncGenerator

import httpx

from language_model_gateway.gateway.http.http_client_factory import HttpClientFactory


class MockHttpClientFactory(HttpClientFactory):
    def __init__(self, *, fn_http_client: Callable[[], httpx.AsyncClient]) -> None:
        self.fn_http_client = fn_http_client
        assert self.fn_http_client is not None

    @asynccontextmanager
    async def create_http_client(
        self, base_url: str
    ) -> AsyncGenerator[httpx.AsyncClient, None]:
        yield self.fn_http_client()