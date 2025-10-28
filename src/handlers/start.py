from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.utils.redis_client import store_jwt_in_redis
from src.external_api.auth_api import register_user
from src.keyboards.keyboards_main import get_main_kb
from src.handlers.dependencies.constant import WELCOME_TEXT

start_router = Router()


@start_router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(WELCOME_TEXT, reply_markup=get_main_kb())
    result = await register_user(message.from_user.id, message.from_user.username)
    if result is None:
        await message.answer("Произошла ошибка при регистрации")
    await store_jwt_in_redis(message.chat.id, result["access_token"])


@start_router.callback_query(StateFilter("*"), F.data.in_(["home"]))
async def home_page(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(WELCOME_TEXT, reply_markup=get_main_kb())
    await state.clear()
    await query.answer()
