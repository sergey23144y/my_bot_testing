from aiogram.fsm.state import StatesGroup, State


class FormOralTask(StatesGroup):
    choosing_task_number = State()  # выбор варианта (38, 39, 40)
    browsing_tasks = State()  # просмотр списка задач внутри варианта
    completing_task = State()  # Выполнение задачи
