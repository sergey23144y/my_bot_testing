import redis.asyncio as aioredis
import logging

from src.core.config import settings

redis_client: aioredis.Redis | None = None
logger = logging.getLogger(__name__)


async def init_redis():
    global redis_client
    redis_client = aioredis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        username=settings.REDIS_USER_NAME,
        password=settings.REDIS_USER_PASSWORD,
    )

    try:
        if await redis_client.ping():
            logger.info("✅ Подключение к Redis успешно!")
        else:
            logger.warning("⚠️ Не удалось подключиться к Redis.")
    except aioredis.RedisError as e:
        logger.error(f"❌ Ошибка подключения к Redis: {e}")


async def close_redis():
    if redis_client:
        await redis_client.close()
        logger.info("🔌 Соединение с Redis закрыто.")


async def store_jwt_in_redis(user_id: str, token: str):
    # Сохраняем в Redis с TTL равным времени жизни токена
    await redis_client.set(f"jwt:{user_id}", token)  # 1 час
    return token


async def get_jwt_from_redis(user_id: int) -> str | None:
    token = await redis_client.get(f"jwt:{user_id}")
    if token:
        return token.decode("utf-8")
    return None
