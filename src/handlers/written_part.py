from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from src.states.form_task import FormTask
from src.handlers.constant import TASKS_TEXT, ALLOWED_TASK_NUMBERS, START_WRITING_TEXT
from src.utils.formatters_written_part import print_task, render_task_page, change_page
from src.external_api.task_api import get_list_task, get_task_by_id
from src.keyboards.kb_base import (
    get_number_tasks_kb,
    get_home_button_kb
)


written_router = Router()


@written_router.message(F.text == "✍️ Письменная часть")
async def writing_handler(message: Message, state: FSMContext):
    await message.answer(START_WRITING_TEXT, reply_markup=ReplyKeyboardRemove())
    await message.answer(TASKS_TEXT, reply_markup=get_number_tasks_kb())
    await state.set_state(FormTask.choosing_task_number)


@written_router.callback_query(
    FormTask.choosing_task_number, F.data.in_(ALLOWED_TASK_NUMBERS)
)
async def page_number_task(query: CallbackQuery, state: FSMContext):
    await state.update_data(number_task=query.data)
    list_task = get_list_task(0, query.data)
    await render_task_page(
        query.message, 0, query.data, str(list_task), list_task.get_total(), state
    )
    await state.set_state(FormTask.browsing_tasks)
    await query.answer()


@written_router.callback_query(
    FormTask.browsing_tasks, F.data.in_(["next_page", "prev_page"])
)
async def page_list_task(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    task_number = int(data.get("number_task"))
    page = data.get("page")
    page = change_page(page, query.data)
    list_task = get_list_task(page, task_number)
    await render_task_page(
        query.message, page, task_number, str(list_task), list_task.get_total(), state
    )
    await query.answer()


@written_router.callback_query(FormTask.browsing_tasks, F.data.startswith("task:"))
async def page_completing_task(query: CallbackQuery, state: FSMContext):
    task_id = int(query.data.split(":")[1])
    await state.update_data(selected_task=task_id)
    data = await state.get_data()
    task_number = int(data.get("number_task"))
    task = get_task_by_id(task_id, task_number)
    await query.message.edit_text(
        print_task(str(task), task_number), reply_markup=get_home_button_kb()
    )

    await query.answer()
    await state.set_state(FormTask.completing_task)


@written_router.message(FormTask.completing_task)
async def handle_task_message(message: Message, state: FSMContext):
    user_answer = message.text
    await state.clear()
    await message.answer(
        f'✅ Ответ сохранён: {user_answer}\n\nРезультаты ответа вы сможете посмотреть в "📊 Мои отчеты" после проверки.',
        reply_markup=get_home_button_kb(),
    )
