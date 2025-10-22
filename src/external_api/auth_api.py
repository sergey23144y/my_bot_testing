import logging
from src.external_api.http_client import http_client


logger = logging.getLogger(__name__)


async def register_user(telegram_id: str, username: str):
    async with http_client as client:
        client.base_url
        response = await client.post(
            "/users", data={"telegram_id": telegram_id, "username": username}
        )
        if response.status_code != 200:
            return None
        try:
            data = response.json()
        except Exception as e:
            logger.error(f"Ошибка при разборе JSON: {e}")
            return None

        logger.info(data)
        return data


async def login_user(telegram_id: str):
    async with http_client as client:
        client.base_url
        response = await client.post(
            "/auth/login", data={"username": telegram_id, "password": " "}
        )
        if response.status_code != 201:
            return None
        try:
            data = response.json()
        except Exception as e:
            logger.error(f"Ошибка при разборе JSON: {e}")
            return None

        return data
