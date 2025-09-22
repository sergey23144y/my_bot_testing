import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.core.config import settings
from src.handlers.start import start_router

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

    logger.info("Starting bot")

    bot: Bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
            # тут ещё много других интересных настроек
        ),
    )
    dp: Dispatcher = Dispatcher()
    dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    # dp.include_router(start.start_router)
    # dp.include_router(orders.orders_router)
    # dp.include_router(lesson.lesson_router)
    dp.include_router(start_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, mylist=[1, 2, 3])


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
