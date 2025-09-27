from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from src.keyboards.kb_report import get_report_actions_kb
from src.states.reporе_state import ReportState
from src.handlers.constant import TASKS_TEXT, ALLOWED_TASK_NUMBERS, START_REPORTS_TEXT
from src.utils.formatters_written_part import change_page
from src.utils.formattesr_reports import render_report_page,print_report
from src.external_api.report_api import get_list_report, get_report_by_id
from src.keyboards.kb_base import get_number_tasks_kb
from src.states.form_task import FormTask

reports_router = Router()


@reports_router.message(F.text == "📊 Мои отчеты")
async def reports_handler(message: Message, state: FSMContext):
    await message.delete()
    await message.answer("Здесь будут ваши отчёты 📊")
    await message.answer(START_REPORTS_TEXT, reply_markup=ReplyKeyboardRemove())
    await message.answer(TASKS_TEXT, reply_markup=get_number_tasks_kb())
    await state.set_state(ReportState.choosing_report_number)


@reports_router.callback_query(
    ReportState.choosing_report_number, F.data.in_(ALLOWED_TASK_NUMBERS)
)
async def page_number_reports(query: CallbackQuery, state: FSMContext):
    await state.update_data(number_task=query.data)
    list_task = get_list_report(0, query.data)
    await render_report_page(
        query.message, 0, query.data, str(list_task), list_task.get_total(), state
    )
    await state.set_state(ReportState.browsing_reports)
    await query.answer()


@reports_router.callback_query(
    ReportState.browsing_reports, F.data.in_(["next_page", "prev_page"])
)
async def page_list_reports(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    task_number = int(data.get("number_task"))
    page = data.get("page")
    page = change_page(page, query.data)
    list_task = get_list_report(page, task_number)
    await render_report_page(
        query.message, page, task_number, str(list_task), list_task.get_total(), state
    )
    await query.answer()


@reports_router.callback_query(
    ReportState.browsing_reports, F.data.startswith("report:")
)
async def page_completing_reports(query: CallbackQuery, state: FSMContext):
    report_id = int(query.data.split(":")[1])
    await state.update_data(selected_task=report_id)
    data = await state.get_data()
    report_number = int(data.get("number_task"))
    report = get_report_by_id(report_id, report_number)
    await query.message.edit_text(
        print_report(report.full_display(), report_number),
        reply_markup=get_report_actions_kb(report.task.id),
    )
    await state.set_state(FormTask.browsing_tasks)

    await query.answer()
