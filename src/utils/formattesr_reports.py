from aiogram.fsm.context import FSMContext
from src.keyboards.kb_base import get_list_items_kb
from src.utils.formatters_written_part import print_tasks


def print_report(
    report_text: str,
    number_task: int,
) -> str:
    return f"📄 Страница отчета\n📌 Вариант задачи: {number_task}\n\n{report_text}\n\n"


async def render_report_page(
    query_or_message,
    page: int,
    task_number: int,
    task_text: str,
    len_task_list: int,
    state: FSMContext,
):
    await state.update_data(page=page)
    await query_or_message.edit_text(
        print_tasks(page, task_number, task_text),
        reply_markup=get_list_items_kb(page, len_task_list, "report"),
    )
