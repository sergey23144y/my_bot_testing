from aiogram.fsm.context import FSMContext
from src.keyboards.kb_base import get_list_items_kb


def print_tasks(page: int, number_task: int, task_text: str) -> str:
    return f"📄 Страница {page + 1}\n📌 Вариант задачи: {number_task}\n\n{task_text}"


def print_task(
    task_text: str,
    number_task: int,
) -> str:
    return (
        f"📄 Страница выполнения задачи\n"
        f"📌 Вариант задачи: {number_task}\n\n"
        f"{task_text}\n\n"
        f"❗Выполните задачу в сообщении. И отправте его❗"
    )


def print_oral_task(
    task_text: str,
    number_task: int,
) -> str:
    return (
        f"📄 Страница выполнения задачи\n"
        f"📌 Вариант задачи: {number_task}\n\n"
        f"{task_text}\n\n"
        f"❗Ответ ожидается в виде голосового сообщения❗"
    )


async def render_task_page(
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
        reply_markup=get_list_items_kb(page, len_task_list),
    )


def change_page(current_page: int, action: str) -> int:
    return current_page + {"next_page": 1, "prev_page": -1}.get(action, 0)
