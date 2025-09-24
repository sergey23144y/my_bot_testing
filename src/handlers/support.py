from aiogram import Router, F
from aiogram.types import Message


support_router = Router()


@support_router.message(F.text == "🛠️ Поддержка")
async def support_handler(message: Message):
    await message.delete()
    await message.answer("Напишите свой вопрос 💬")
