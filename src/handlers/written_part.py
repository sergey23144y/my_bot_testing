from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from src.handlers.dependencies.send_message import send_error_message
from src.core.enums import NumberTask, TaskType
from src.handlers.dependencies.filters import NumberTaskFilter
from src.handlers.dependencies.constant import (
    WRITING_TASKS_TEXT,
    START_WRITING_TEXT,
)
from src.states.form_task import FormTask
from src.handlers.dependencies.formatters_task import (
    print_task,
    render_task_page,
    change_page,
)
from src.external_api.task_api import fetch_list_task, fetch_task_by_id, send_solutions
from src.keyboards.kb_base import get_number_tasks_kb, get_home_button_kb


written_router = Router()


@written_router.message(F.text == "✍️ Письменная часть")
async def writing_handler(message: Message, state: FSMContext):
    await message.answer(START_WRITING_TEXT, reply_markup=ReplyKeyboardRemove())
    await message.answer(WRITING_TASKS_TEXT, reply_markup=get_number_tasks_kb())
    await state.set_state(FormTask.choosing_task_number)


@written_router.callback_query(FormTask.choosing_task_number, NumberTaskFilter())
async def page_number_task(query: CallbackQuery, number: NumberTask, state: FSMContext):
    await state.update_data(number=number.to_json())

    list_task = await fetch_list_task(
        1, number=number, type=TaskType.WRITING, telegram_id=query.from_user.id
    )

    if not list_task:
        await send_error_message(query, "❌ Не удалось загрузить список заданий.")
        return

    await render_task_page(query.message, 1, number, list_task, state)
    await state.set_state(FormTask.browsing_tasks)
    await query.answer()


@written_router.callback_query(
    FormTask.browsing_tasks, F.data.in_(["next_page", "prev_page"])
)
async def page_list_task(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    try:
        task_number = NumberTask.from_json(data.get("number"))
        page = int(data.get("page", 1))
    except Exception:
        await send_error_message(
            query, "⚠ Ошибка данных состояния. Попробуйте начать заново."
        )
        await state.clear()
        return

    page = change_page(page, query.data)
    list_task = await fetch_list_task(
        page, number=task_number, type=TaskType.WRITING, telegram_id=query.from_user.id
    )

    if not list_task:
        await send_error_message(query, "❌ Не удалось загрузить задания.")
        return

    await render_task_page(query.message, page, task_number, list_task, state)
    await query.answer()


@written_router.callback_query(FormTask.browsing_tasks, F.data.startswith("task:"))
async def page_completing_task(query: CallbackQuery, state: FSMContext):
    task_id = int(query.data.split(":")[1])
    await state.update_data(selected_task=task_id)

    data = await state.get_data()
    try:
        task_number = NumberTask.from_json(data.get("number"))
    except Exception:
        await send_error_message(query, "⚠ Ошибка состояния. Начните заново.")
        await state.clear()
        return

    task = await fetch_task_by_id(task_id, telegram_id=query.from_user.id)
    if not task:
        await send_error_message(query, "❌ Не удалось загрузить задание.")
        return

    await query.message.edit_text(
        print_task(task.to_string(), task_number), reply_markup=get_home_button_kb()
    )

    await query.answer()
    await state.set_state(FormTask.completing_task)


@written_router.message(FormTask.completing_task)
async def handle_task_message(message: Message, state: FSMContext):
    user_answer = message.text
    data = await state.get_data()
    selected_task = int(data.get("selected_task"))

    if not selected_task:
        await send_error_message(
            message, "⚠ Ошибка состояния. Попробуйте выбрать задание заново."
        )
        await state.clear()
        return

    result = await send_solutions(message.from_user.id, selected_task, user_answer)
    if result:
        await message.answer(
            f"✅ Ответ сохранён: {user_answer}\n\n"
            'Результаты ответа вы сможете посмотреть в "📊 Мои отчеты" после проверки.',
            reply_markup=get_home_button_kb(),
        )
    else:
        await message.answer(
            "❌ Ошибка отправки ответа",
            reply_markup=get_home_button_kb(),
        )
    await state.clear()
