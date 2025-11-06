from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from src.core.enums import TaskType
from src.schemas.Task.task_model import TaskModel
from src.utils.text import escape_text_from_admin_panel


class SolutionModal(BaseModel):
    id: int
    content: str
    created_at: datetime = Field(alias="created_at")
    task_id: int
    task: Optional[TaskModel] = None


class ReportModel(BaseModel):
    id: int
    solution: SolutionModal
    mark: int | None
    analysis: str | None

    def to_string(self) -> str:
        """Возвращает читаемое строковое представление задачи"""
        return (
            f"{'🎤' if (self.solution.task.type == TaskType.WRITING) else '📝'} <b>Задание:</b> {self.solution.task.title}\n"
            f"📅 <b>Дата решения:</b> {self.solution.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"🔄 <b>Статус:</b> {'✅Проверено' if self.mark else '⏳ В процессе проверки'}\n"
            f"✨ <b>Оценка:</b> {self.mark if self.mark else '-'}\n"
        )

    def full_display(self) -> str:
        """Возвращает читаемое строковое представление задачи для пользователя (id не включается)"""
        # Эмодзи для типа задачи
        type_emoji = "🎤" if self.solution.task.type == TaskType.WRITING else "📝"

        # Статус выполнения
        status = "✅ Завершено" if self.mark is not None else "⏳ В процессе"

        # Оценка в виде звезд
        rating = self.mark if self.mark is not None else "-"

        # Формируем текст
        return (
            f"{type_emoji} <b>Задание</b>: {self.solution.task.title}\n"
            f"📅 <b>Дата решения:</b> {self.solution.created_at}\n"
            f"🔄 <b>Статус:</b> {status}\n"
            f"✨ <b>Оценка:</b> {rating}\n\n"
            f"📝 <b>Ваше решение:</b>\n<i>{self.solution.content}</i>\n\n"
            f"📃 <b>Анализ решения:</b>\n<i>{escape_text_from_admin_panel(self.analysis) if self.analysis else '-'}</i>"
        )


class ReportListModel(BaseModel):
    reports: List[ReportModel] = Field(alias="data")
    total: int

    def get_by_id(self, report_id: int) -> Optional[ReportModel]:
        """Получить задачу по id"""
        return next((report for report in self.reports if report.id == report_id), None)

    def get_total(self) -> int:
        return self.total

    def to_string(self) -> str:
        return "\n\n".join(report.to_string() for report in self.reports)
