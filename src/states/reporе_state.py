from aiogram.fsm.state import StatesGroup, State


class ReportState(StatesGroup):
    browsing_reports = State()  # просмотр списка задач внутри варианта
    completing_report = State()  # Выполнение задачи
