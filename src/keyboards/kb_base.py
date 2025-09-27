from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from src.utils.digit_emojis import number_to_digit_emojis


def get_list_items_kb(page: int, len_task_list: int, prefix: str = "task"):
    """
    Генерация клавиатуры пагинации для списка элементов.

    :param page: текущая страница
    :param total_items: общее количество элементов (tasks/reports/...)
    :param prefix: префикс для callback_data ("task", "report", ...)
    """
    builder = InlineKeyboardBuilder()
    kb_row = []
    # Кнопки с номерами элементов
    for i in range((page) * 5, (page + 1) * 5):
        if i >= len_task_list:  # ✅ проверка выхода за пределы
            break
        kb_row.append(
            InlineKeyboardButton(
                text=number_to_digit_emojis(i + 1), callback_data=f"{prefix}:{i}"
            )
        )
    if kb_row:
        builder.row(*kb_row)
        kb_row = []
    # Кнопки пагинации
    if page > 0:
        kb_row.append(InlineKeyboardButton(text="⬅ Назад", callback_data="prev_page"))
    if (page + 1) * 5 < len_task_list:
        kb_row.append(InlineKeyboardButton(text="Вперёд ➡", callback_data="next_page"))

    if kb_row:
        builder.row(*kb_row)
    # Кнопка "домой"
    builder.row(InlineKeyboardButton(text="🏚 На главную", callback_data="home"))
    return builder.as_markup()


def get_number_tasks_kb():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text=number_to_digit_emojis(38), callback_data="38"),
        InlineKeyboardButton(text=number_to_digit_emojis(39), callback_data="39"),
        InlineKeyboardButton(text=number_to_digit_emojis(40), callback_data="40"),
    )

    builder.row(InlineKeyboardButton(text="🏚 На главную", callback_data="home"))
    return builder.as_markup()


def get_home_button_kb():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="🏚 На главную", callback_data="home"))
    return builder.as_markup()
