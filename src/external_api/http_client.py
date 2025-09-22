from httpx import AsyncClient
from core.config import settings


class AsyncHTTPClient:
    def __init__(self, base_url):
        self.base_url = base_url

    async def __aenter__(self) -> AsyncClient:
        self.client = AsyncClient(
            base_url=self.base_url,
            timeout=120.0,
        )
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()


http_client = AsyncHTTPClient(base_url=settings.api_url)
