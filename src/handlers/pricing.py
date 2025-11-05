from aiogram import Router, F
from aiogram.types import CallbackQuery
from src.keyboards.kb_base import get_home_button_kb


pricing_router = Router()


@pricing_router.callback_query(F.data == "Тарифы")
async def tariffs_handler(query: CallbackQuery):
    await query.message.edit_text(
        "💳 Этот раздел находится в разработке!",
        reply_markup=get_home_button_kb(),
    )
