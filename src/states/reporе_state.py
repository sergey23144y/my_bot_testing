from aiogram.fsm.state import StatesGroup, State


class ReportState(StatesGroup):
    choosing_report_number = State()  # выбор варианта (38, 39, 40)
    browsing_reports = State()  # просмотр списка задач внутри варианта
    completing_report = State()  # Выполнение задачи
