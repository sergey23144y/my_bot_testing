from aiogram import Router, F
from aiogram.types import Message

from src.external_api.task_api import fetch_list_task


pricing_router = Router()


@pricing_router.message(F.text == "💳 Тарифы")
async def tariffs_handler(message: Message):
    tasks = await fetch_list_task()
    await message.delete()
    if not tasks:
        await message.answer("Нет данных для отображения")
    else:
        await message.answer(str(tasks))

    tasks = await fetch_list_task()
    await message.delete()
    if not tasks:
        await message.answer("Нет данных для отображения")
    else:
        await message.answer(str(tasks))
