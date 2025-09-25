import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.core.config import settings
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
