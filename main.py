import asyncio
import logging
from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from datetime import datetime

from src.handlers import main_router
from src.core.config import settings, bot
from src.utils.redis_client import init_redis

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )
    await init_redis()
    logger.info("Starting bot")

    storage = RedisStorage.from_url(settings.ger_redis_url())
    dp: Dispatcher = Dispatcher(storage=storage)
    dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    dp.include_router(main_router.routers)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
