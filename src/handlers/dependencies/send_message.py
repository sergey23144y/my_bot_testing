from aiogram.types import CallbackQuery

from src.keyboards.kb_base import get_home_button_kb


async def send_error_message(message_or_query, text: str):
    """Универсальная отправка сообщения об ошибке."""
    target = (
        message_or_query.message
        if isinstance(message_or_query, CallbackQuery)
        else message_or_query
    )
    await target.answer(text, reply_markup=get_home_button_kb())
