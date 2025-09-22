from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from src.keyboards.keyboards_main import get_main_kb

start_router = Router()


@start_router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        """
👨‍🎓 Добро пожаловать в платформу подготовки к ЕГЭ по английскому языку!

Здесь ты найдёшь всё необходимое для эффективной подготовки:
📊 Мои отчёты — отслеживай свой прогресс.
📝 Письменная часть — практикуй эссе, письма и другие письменные задания.
🎤 Устная часть — тренируй устные ответы по формату ЕГЭ.
🤖 AI Рерайтер — переформулируй свои тексты с помощью умного ассистента.
📘 Примеры выполнения — изучай лучшие образцы высоко оценённых работ.
💬 Поддержка — помощь и обратная связь.
💰 Тарифы — выбери подходящий план и получи больше возможностей.
➡️ Начни с любого раздела и двигайся к высокому результату на экзамене!

""",
        reply_markup=get_main_kb(),
    )


@start_router.message(F.text == "✍️ Письменая чать")
async def writing_handler(message: Message):
    await message.delete()
    await message.answer("Раздел для письменных заданий 📝")


@start_router.message(F.text == "🎤 Устная часть")
async def speaking_handler(message: Message):
    await message.delete()
    await message.answer("Здесь тренируем устную часть 🎤")


@start_router.message(F.text == "🤖 AI Рерайтинг")
async def rewriter_handler(message: Message):
    await message.delete()
    await message.answer("Переформулировка текста 🤖")


@start_router.message(F.text == "📚 Примеры выполнения")
async def examples_handler(message: Message):
    await message.delete()
    await message.answer("Образцы работ 📘")


@start_router.message(F.text == "🛠️ Поддержка")
async def support_handler(message: Message):
    await message.delete()
    await message.answer("Напишите свой вопрос 💬")


@start_router.message(F.text == "💳 Тарифы")
async def tariffs_handler(message: Message):
    await message.delete()
    await message.answer("Информация о тарифах 💰")
