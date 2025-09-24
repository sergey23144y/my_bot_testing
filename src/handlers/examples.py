from aiogram import Router, F
from aiogram.types import Message


examples_router = Router()


@examples_router.message(F.text == "📚 Примеры выполнения")
async def examples_handler(message: Message):
    await message.delete()
    await message.answer("Здесь будут примеры готовых работ для разбора")
