from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from typing import Sequence, TypeVar
from src.core.enums import NumberTask
from src.utils.digit_emojis import number_to_digit_emojis


T = TypeVar("T")


def get_list_items_kb(
    page: int,
    items: Sequence[T],
    total_count: int,
    page_size: int = 5,
    prefix: str = "task",
):
    """
    Генерация клавиатуры пагинации для списка элементов.

    :param page: текущая страница
    :param total_items: общее количество элементов (tasks/reports/...)
    :param prefix: префикс для callback_data ("task", "report", ...)
    """
    builder = InlineKeyboardBuilder()
    kb_row = []
    # 🟦 1. Кнопки с элементами
    if items:
        buttons = [
            InlineKeyboardButton(
                text=number_to_digit_emojis(index + 1),
                callback_data=f"{prefix}:{getattr(item, 'id', 0)}",
            )
            for index, item in enumerate(items)
        ]
        builder.row(*buttons)

    if kb_row:
        builder.row(*kb_row)
        kb_row = []

    # Кнопки пагинации
    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(
            InlineKeyboardButton(text="⬅ Назад", callback_data="prev_page")
        )
    if page * page_size < total_count:
        pagination_buttons.append(
            InlineKeyboardButton(text="Вперёд ➡", callback_data="next_page")
        )

    if pagination_buttons:
        builder.row(*pagination_buttons)

    if kb_row:
        builder.row(*kb_row)
    # Кнопка "домой"

    builder.row(InlineKeyboardButton(text="🏚 На главную", callback_data="home"))
    return builder.as_markup()


def get_number_tasks_kb():
    builder = InlineKeyboardBuilder()

    builder.row(
        *[
            InlineKeyboardButton(
                text=number_to_digit_emojis(task.number), callback_data=task.number
            )
            for task in NumberTask
        ]
    )

    builder.row(InlineKeyboardButton(text="🏚 На главную", callback_data="home"))
    return builder.as_markup()


def get_home_button_kb():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="🏚 На главную", callback_data="home"))
    return builder.as_markup()
