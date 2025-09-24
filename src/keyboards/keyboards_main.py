from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


def get_main_kb():
    kb_main = ReplyKeyboardBuilder()

    kb_main.row(KeyboardButton(text="📊 Мои отчеты"))
    kb_main.row(
        KeyboardButton(text="✍️ Письменная часть"),
        KeyboardButton(text="🎤 Устная часть"),
    )
    kb_main.row(
        KeyboardButton(text="🤖 AI Рерайтинг"),
        KeyboardButton(text="📚 Примеры выполнения"),
    )
    kb_main.row(
        KeyboardButton(text="🛠️ Поддержка"),
        KeyboardButton(text="💳 Тарифы"),
    )
    return kb_main.as_markup(resize_keyboard=True)
