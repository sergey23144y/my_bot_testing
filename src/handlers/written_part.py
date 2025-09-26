from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from src.keyboards.kb_written import (
    get_written_list_task_kb,
    get_written_number_tasks_kb,
    get_task_actions_kb,
)
from src.states.form_task import FormTask
from src.external_api.task_api import get_list_task, get_task_by_id
from src.schemas.taskDTO import format_task


TASKS_TEXT = """✨ Выберите задание:

1️⃣ 38 — 📘 Задание  
2️⃣ 39 — 📝 Задание  
3️⃣ 40 — 🎯 Задание  

💡 Нажмите на нужный номер, чтобы продолжить.
"""


def print_tasks(page: int, number_task: int) -> str:
    page_items = get_list_task(page, number_task, limit_page=5)
    tasks = "\n\n".join(format_task(item) for item in page_items)

    return f"📄 Страница {page + 1}\n📌 Вариант задачи: {number_task}\n\n{tasks}"


def print_task(task_id: int, number_task: int) -> str:
    return (
        f"📄 Страница выполнения задачи\n"
        f"📌 Вариант задачи: {number_task}\n\n"
        f"{format_task(get_task_by_id(task_id, number_task))}"
        f"❗❗❗Выполните задачу в сообщении. И отправте его❗❗❗"
    )


written_router = Router()


@written_router.message(F.text == "✍️ Письменная часть")
async def writing_handler(message: Message, state: FSMContext):
    await message.answer(
        "Сдесь вы выполняите задания из ЕГЭ",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(
        TASKS_TEXT,
        reply_markup=get_written_number_tasks_kb(),
    )
    await state.set_state(FormTask.choosing_task_number)


@written_router.callback_query(
    FormTask.choosing_task_number, F.data.in_(["38", "39", "40"])
)
async def page_number_task(query: CallbackQuery, state: FSMContext):
    await state.update_data(number_task=query.data)
    data = await state.get_data()
    await query.message.edit_text(
        print_tasks(0, int(data.get("number_task"))),
        reply_markup=get_written_list_task_kb(0),
    )

    await state.set_state(FormTask.browsing_tasks)
    await query.answer()


@written_router.callback_query(
    FormTask.browsing_tasks, F.data.in_(["next_page", "prev_page"])
)
async def page_list_task(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    task_number = int(data.get("number_task"))
    page = data.get("page", 0)

    if query.data == "next_page":
        page += 1
    elif query.data == "prev_page":
        page -= 1

    await state.update_data(page=page)

    await query.message.edit_text(
        print_tasks(page, task_number), reply_markup=get_written_list_task_kb(page)
    )
    await query.answer()


@written_router.callback_query(FormTask.browsing_tasks, F.data.startswith("task:"))
async def page_completing_task(query: CallbackQuery, state: FSMContext):
    task_id = int(query.data.split(":")[1])
    await state.update_data(selected_task=task_id)
    data = await state.get_data()
    task_number = int(data.get("number_task"))

    await query.message.edit_text(
        print_task(task_id, task_number), reply_markup=get_task_actions_kb()
    )
    await query.answer()
    await state.set_state(FormTask.completing_task)


@written_router.message(FormTask.completing_task)
async def handle_task_message(message: Message, state: FSMContext):
    user_answer = message.text
    await state.clear()
    await message.answer(
        f'✅ Ответ сохранён: {user_answer}\n\nРезультаты ответа вы сможете посмотреть в "📊 Мои отчеты" после проверки.',
        reply_markup=get_task_actions_kb(),
    )
