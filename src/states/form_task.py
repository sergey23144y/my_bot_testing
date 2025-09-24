from aiogram.fsm.state import StatesGroup, State


class Form_task(StatesGroup):
    number_task = State()
    in_task = State()