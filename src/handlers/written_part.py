from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from src.keyboards.kb_written import (
    get_page_text,
    get_written_list_task_kb,
    get_written_number_tasks_kb,
)
from src.keyboards.keyboards_main import get_main_kb
from src.states.form_task import Form_task

written_router = Router()


@written_router.message(F.text == "✍️ Письменная часть")
async def writing_handler(message: Message, state: FSMContext):
    await message.answer(
        """Выберите задания: 
        38 - Задание
        39 - Заданиеs
        40 - Задание
        """,
        reply_markup=get_written_number_tasks_kb(),
    )
    await state.set_state(Form_task.number_task)


@written_router.callback_query(Form_task.number_task, F.data.in_(["38", "39", "40"]))
async def page_number_task(query: CallbackQuery, state: FSMContext):
    await state.update_data(number_task=query.data)
    data = await state.get_data()
    await query.message.edit_text(
        get_page_text(0, int(data.get("number_task"))),
        reply_markup=get_written_list_task_kb(0),
    )

    await state.set_state(Form_task.in_task)
    await query.answer()


@written_router.callback_query(
    Form_task.in_task, F.data.in_(["next_page", "prev_page"])
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
        get_page_text(page, task_number), reply_markup=get_written_list_task_kb(page)
    )
    await query.answer()


@written_router.callback_query(StateFilter("*"), F.data.in_(["home"]))
async def cmd_start(query: CallbackQuery, state: FSMContext):
    await query.message.answer(
        """
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
