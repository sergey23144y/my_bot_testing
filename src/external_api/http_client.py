import logging
from typing import Optional
from httpx import AsyncClient, AsyncHTTPTransport, Request, Response
from src.core.config import settings

logger = logging.getLogger("http_client")


class AsyncHTTPClient:
    def __init__(self, base_url, safe_logging: bool = True):
        if not base_url:
            raise ValueError("API_URL не задан!")
        if not base_url.startswith(("http://", "https://")):
            base_url = "http://" + base_url  # добавляем протокол по умолчанию
        self.base_url = base_url
        self.safe_logging = safe_logging
        self.transport = AsyncHTTPTransport(retries=0, proxy=None)
        self.client: Optional[AsyncClient] = None

    async def __aenter__(self) -> AsyncClient:
        async def log_request(request: Request):
            logger.debug(f"HTTP Request: {request.method} {request.url}")
            if not self.safe_logging and request.content:
                logger.debug(f"Request body: {request.content}")

        async def log_response(response: Response):
            logger.debug(
                f"HTTP Response: {response.status_code} {response.request.method} {response.request.url}"
            )
            if not self.safe_logging:
                logger.debug(f"Response body: {response.text[:500]}")

        self.client = AsyncClient(
            base_url=self.base_url,
            timeout=120.0,
            transport=self.transport,
            event_hooks={
                "request": [log_request],
            },
        )
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def close(self):
        if self.client and not self.client.is_closed:
            await self.client.aclose()


http_client = AsyncHTTPClient(base_url=settings.API_URL)
