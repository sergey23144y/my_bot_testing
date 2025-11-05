from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from src.handlers.dependencies.send_message import send_error_message
from src.keyboards.kb_report import get_report_actions_kb
from src.states.reporе_state import ReportState
from src.handlers.dependencies.constant import (
    START_REPORTS_TEXT,
)
from src.handlers.dependencies.formatters_task import change_page
from src.handlers.dependencies.formattesr_reports import (
    send_or_edit_report,
    print_report,
)
from src.external_api.report_api import fetch_list_report, fetch_report_by_id
from src.states.form_task import FormTask

reports_router = Router()


async def page_number_reports(query: CallbackQuery, state: FSMContext, page: int = 1):
    message = query.message
    list_report = await fetch_list_report(message.chat.id, page)
    if not list_report:
        await send_error_message(message, "❌ Не удалось загрузить список отчетов.")
        return
    if len(list_report.reports) == 0 or not list_report.reports:
        await send_error_message(message, "⚠ У вас еще нет отчетов")
        return

    await send_or_edit_report(query, page, list_report, state, "edit")


@reports_router.callback_query(F.data == "Отчеты")
async def reports_handler(query: CallbackQuery, state: FSMContext):
    # await query.message.edit_text(
    #     START_REPORTS_TEXT
    # )
    await page_number_reports(query, state)
    await state.set_state(ReportState.browsing_reports)


@reports_router.callback_query(
    ReportState.browsing_reports, F.data.in_(["next_page", "prev_page"])
)
async def page_list_reports(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        page = data.get("page")
    except Exception:
        await send_error_message(
            query, "⚠ Ошибка данных состояния. Попробуйте начать заново."
        )
        await state.clear()
        return

    page = change_page(page, query.data)
    await page_number_reports(query, state, page)

    await query.answer()


@reports_router.callback_query(
    ReportState.browsing_reports, F.data.startswith("report:")
)
async def page_completing_reports(query: CallbackQuery, state: FSMContext):
    report_id = int(query.data.split(":")[1])
    report = await fetch_report_by_id(query.from_user.id, report_id)
    if not report:
        await send_error_message(
            query, "⚠ Ошибка получения данных. Попробуйте начать заново."
        )
        return

    # await state.update_data(number=report.task.number.to_json())

    await query.message.edit_text(
        print_report(report.full_display()),
        reply_markup=get_report_actions_kb(report.solution.task_id),
    )

    await state.set_state(FormTask.browsing_tasks)
    await query.answer()
