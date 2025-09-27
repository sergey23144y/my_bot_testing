from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from src.keyboards.keyboards_main import get_main_kb
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from src.handlers.constant import WELCOME_TEXT

start_router = Router()


@start_router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(WELCOME_TEXT, reply_markup=get_main_kb())


@start_router.callback_query(StateFilter("*"), F.data.in_(["home"]))
async def home_page(query: CallbackQuery, state: FSMContext):
    await query.message.answer(WELCOME_TEXT, reply_markup=get_main_kb())
    await state.clear()
    await query.answer()
