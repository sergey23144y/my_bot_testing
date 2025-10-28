from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def get_main_kb():
    kb_main = InlineKeyboardBuilder()

    kb_main.row(InlineKeyboardButton(text="📊 Мои отчеты", callback_data="Отчеты"))
    kb_main.row(
        InlineKeyboardButton(text="✍️ Письменная часть", callback_data="Письменная"),
        InlineKeyboardButton(text="🎤 Устная часть", callback_data="Устная"),
    )
    kb_main.row(
        InlineKeyboardButton(text="🤖 AI Рерайтинг", callback_data="Рерайтинг"),
        InlineKeyboardButton(text="📚 Примеры выполнения", callback_data="Примеры"),
    )
    kb_main.row(
        InlineKeyboardButton(text="🛠️ Поддержка", callback_data="Поддержка"),
        InlineKeyboardButton(text="💳 Тарифы", callback_data="Тарифы"),
    )
    return kb_main.as_markup(resize_keyboard=True)
