import logging
from typing import Optional, Type, TypeVar
from httpx import Response
from src.utils.redis_client import get_jwt_from_redis
from src.external_api.http_client import http_client


logger = logging.getLogger(__name__)


T = TypeVar("T")


async def _make_request(
    telegram_id: str,
    method: str,
    endpoint: str,
    model: Type[T],
    **kwargs,
) -> Optional[T]:
    """Универсальный HTTP-запрос с авторизацией и обработкой ошибок."""
    token = await get_jwt_from_redis(telegram_id)
    headers = {"Authorization": f"Bearer {token}"}
    kwargs.setdefault("headers", headers)

    async with http_client as client:
        try:
            response: Response = await client.request(method, endpoint, **kwargs)
            response.raise_for_status()
        except Exception as e:
            logger.error(
                f"Ошибка при выполнении запроса {method.upper()} {endpoint}: {e}"
            )
            return None

        try:
            data = response.json()
        except Exception as e:
            logger.error(f"Ошибка при разборе JSON для {endpoint}: {e}")
            return None

        try:
            return model(**data)
        except Exception as e:
            logger.error(f"Ошибка при инициализации модели {model.__name__}: {e}")
            return None
