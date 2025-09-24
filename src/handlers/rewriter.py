from aiogram import Router, F
from aiogram.types import Message


rewriter_router = Router()


@rewriter_router.message(F.text == "🤖 AI Рерайтинг")
async def rewriter_handler(message: Message):
    await message.delete()
    await message.answer("Переформулировка текста 🤖")
