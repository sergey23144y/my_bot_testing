import logging
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from src.schemas.Report.report_model import ReportListModel
from src.keyboards.kb_base import get_list_items_kb

logger = logging.getLogger(__name__)


def print_report(report_text: str) -> str:
    return (
        f"📄 <i>Страница отчета</i>\n\n"
        f"{report_text}\n\n"
    )


async def send_or_edit_report(
    query_or_message: Message | CallbackQuery,
    page: int,
    data: ReportListModel,
    state: FSMContext,
    mode: str = "edit",  # "edit" или "answer"
):
    await state.update_data(page=page)

    logger.info(f"Отправка отчета в {type(data.get_total())}")
    text = print_reports(page, data.to_string())
    keyboard = get_list_items_kb(page, data.reports, data.get_total(), prefix="report")

    if mode == "edit" and isinstance(query_or_message, CallbackQuery):
        await query_or_message.message.edit_text(text, reply_markup=keyboard)
    else:
        await query_or_message.answer(text, reply_markup=keyboard)


def print_reports(page: int, task_text: str) -> str:
    return (
        f"📄 <i>Страница {page}</i>\n\n"
        f"{task_text}"
    )
