from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from src.core.digit_emojis import number_to_digit_emojis
from src.schemas.MockData import items


def get_written_kb(page: int):
    """Генерация клавиатуры пагинации"""
    builder = InlineKeyboardBuilder()
    kb_row = []
    for i in range((page) * 5, (page + 1) * 5):
        if i >= len(items):  # ✅ проверка выхода за пределы
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
        kb_row.append(
            InlineKeyboardButton(text="⬅ Назад", callback_data=f"page:{page - 1}")
        )
    if (page + 1) * 5 < len(items):
        kb_row.append(
            InlineKeyboardButton(text="Вперёд ➡", callback_data=f"page:{page + 1}")
        )

    if kb_row:
        builder.row(*kb_row)
    return builder.as_markup()


def get_page_text(page: int):
    """Формируем текст страницы"""
    start = page * 5
    end = start + 5
    page_items = items[start:end]
    text = "\n".join(page_items)
    return f"📄 Страница {page + 1}\n\n{text}"
