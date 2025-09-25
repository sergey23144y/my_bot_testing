from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from src.core.digit_emojis import number_to_digit_emojis
from src.schemas.mock_data import items_38


def get_written_list_task_kb(page: int):
    """Генерация клавиатуры пагинации"""
    builder = InlineKeyboardBuilder()
    kb_row = []
    for i in range((page) * 5, (page + 1) * 5):
        if i >= len(items_38):  # ✅ проверка выхода за пределы
            break
        kb_row.append(
            InlineKeyboardButton(
                text=number_to_digit_emojis(i + 1), callback_data=f"task:{i}"
            )
        )
    if kb_row:
        builder.row(*kb_row)
        kb_row = []
    # Кнопки «Назад» и «Вперёд»
    if page > 0:
        kb_row.append(InlineKeyboardButton(text="⬅ Назад", callback_data="prev_page"))
    if (page + 1) * 5 < len(items_38):
        kb_row.append(InlineKeyboardButton(text="Вперёд ➡", callback_data="next_page"))

    if kb_row:
        builder.row(*kb_row)

    builder.row(InlineKeyboardButton(text="🏚 На главную", callback_data="home"))
    return builder.as_markup()


def get_written_number_tasks_kb():
    """Генерация клавиатуры пагинации"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text=number_to_digit_emojis(38), callback_data="38"),
        InlineKeyboardButton(text=number_to_digit_emojis(39), callback_data="39"),
        InlineKeyboardButton(text=number_to_digit_emojis(40), callback_data="40"),
    )

    builder.row(InlineKeyboardButton(text="🏚 На главную", callback_data="home"))
    return builder.as_markup()


