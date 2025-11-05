from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.keyboards.kb_base import get_home_button_kb


examples_router = Router()


@examples_router.callback_query(F.data == "Примеры")
async def examples_handler(query: CallbackQuery):
    await query.message.answer(
        "Здесь будут примеры решения заданий",
        reply_markup=get_home_button_kb(),
    )
