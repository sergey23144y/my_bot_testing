import logging
from aiogram.fsm.context import FSMContext
from src.schemas.Task.task_model import TaskListModel
from src.core.enums import NumberTask
from src.keyboards.kb_base import get_list_items_kb

logger = logging.getLogger(__name__)


def print_tasks(page: int, number_task: NumberTask, task_text: str) -> str:
    return (
        f"📄 <i>Страница {page}</i>\n\n"
        f"📌 <b>Задание:</b> {number_task.description}\n\n"
        f"{task_text}"
    )


def print_task(
    task_text: str,
    number_task: NumberTask,
) -> str:
    return (
        f"📄 <i>Страница выполнения задания</i>\n\n"
        f"📌 <b>Задание:</b> {number_task.description}\n\n"
        f"{task_text}\n\n"
        f"❗Отправьте решение задания в текстовом сообщении"
    )


def print_oral_task(
    task_text: str,
    number_task: NumberTask,
) -> str:
    return (
        f"📄 <i>Страница выполнения задания</i>\n\n"
        f"📌 Задачи: {number_task.description}\n\n"
        f"{task_text}\n\n"
        f"❗Отправьте решение задания в голосовом сообщении"
    )


async def render_task_page(
    query_or_message,
    page: int,
    task_number: NumberTask,
    tasks: TaskListModel,
    state: FSMContext,
):
    await state.update_data(page=page)
    await query_or_message.edit_text(
        print_tasks(page, task_number, tasks.to_string()),
        reply_markup=get_list_items_kb(page, tasks.tasks, tasks.get_total()),
    )


def change_page(current_page: int, action: str) -> int:
    return current_page + {"next_page": 1, "prev_page": -1}.get(action, 0)
