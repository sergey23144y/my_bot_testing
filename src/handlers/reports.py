from aiogram import Router, F
from aiogram.types import Message


reports_router = Router()


@reports_router.message(F.text == "📊 Мои отчеты")
async def reports_handler(message: Message):
    await message.delete()
    await message.answer("Здесь будут ваши отчёты 📊")
