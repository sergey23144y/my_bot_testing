import asyncio
import logging
import redis
from aiogram import Bot, Dispatcher
from src.core.config import settings
from aiogram.fsm.storage.redis import RedisStorage
from src.handlers import (
    start,
    examples,
    oral_part,
    pricing,
    reports,
    rewriter,
    support,
    written_part,
)

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from datetime import datetime

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    r = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        username=settings.redis_user_name,
        password=settings.redis_user_password,
    )

    try:
        info = r.info()
        print(info["redis_version"])
        response = r.ping()
        if response:
            print("Подключение успешно!")
        else:
            print("Не удалось подключиться к Redis.")
    except redis.exceptions.RedisError as e:
        print(f"Ошибка: {e}")

    logger.info("Starting bot")

    bot: Bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
            # тут ещё много других интересных настроек
        ),
    )

    storage = RedisStorage.from_url(settings.ger_redis_url())
    dp: Dispatcher = Dispatcher(storage=storage)
    dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    dp.include_router(written_part.written_router)
    dp.include_router(start.start_router)
    dp.include_router(examples.examples_router)
    dp.include_router(oral_part.oral_router)
    dp.include_router(pricing.pricing_router)
    dp.include_router(reports.reports_router)
    dp.include_router(rewriter.rewriter_router)
    dp.include_router(support.support_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
