from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def get_report_actions_kb(task_ID: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔄 Решить снова", callback_data=f"task:{task_ID}")
    )
    builder.row(InlineKeyboardButton(text="🏚 На главную", callback_data="home"))
    return builder.as_markup()
