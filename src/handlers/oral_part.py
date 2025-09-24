from aiogram import Router, F
from aiogram.types import Message


oral_router = Router()


@oral_router.message(F.text == "🎤 Устная часть")
async def speaking_handler(message: Message):
    await message.delete()
    await message.answer("🎤 На данный момент функционал реализовывается")
