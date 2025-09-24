from aiogram import Router, F
from aiogram.types import Message


pricing_router = Router()


@pricing_router.message(F.text == "💳 Тарифы")
async def tariffs_handler(message: Message):
    await message.delete()
    await message.answer("Информация о тарифах 💰")
