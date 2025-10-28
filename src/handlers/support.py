from aiogram import Router, F
from aiogram.types import CallbackQuery
from src.keyboards.kb_base import get_home_button_kb


support_router = Router()


@support_router.callback_query(F.data == "Поддержка")
async def support_handler(query: CallbackQuery,):
    await query.message.edit_text(
        "Напишите свой вопрос 💬", reply_markup=get_home_button_kb()
    )
