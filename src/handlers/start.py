from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
from src.keyboards.keyboards_main import get_main_kb
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

start_router = Router()


@start_router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Клавиатура убрана ✅", reply_markup=ReplyKeyboardRemove())
    await message.delete()
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


@start_router.callback_query(StateFilter("*"), F.data.in_(["home"]))
async def home_page(query: CallbackQuery, state: FSMContext):
    await query.message.answer(
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

    await state.clear()
    await query.answer()
