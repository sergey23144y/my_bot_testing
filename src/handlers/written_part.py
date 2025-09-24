from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from src.keyboards.kb_written import get_page_text, get_written_kb

written_router = Router()


@written_router.message(F.text == "✍️ Письменная часть")
async def writing_handler(message: Message):
    await message.delete()
    await message.answer(get_page_text(0), reply_markup=get_written_kb(0))


@written_router.callback_query(F.data.startswith("page:"))
async def page_callback(query: CallbackQuery):
    page = int(query.data.split(":")[1])
    await query.message.edit_text(
        get_page_text(page), reply_markup=get_written_kb(page)
    )
    await query.answer()  # убираем «часики» на кнопке
