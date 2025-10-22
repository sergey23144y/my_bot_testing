from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from src.core.enums import TaskType
from src.schemas.Task.task_model import TaskModel


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
            f"📅{self.solution.created_at} | {'🎤' if (self.solution.task.type == TaskType.WRITING) else '📝'} {self.solution.task.title}\n"
            f"🔄Статус: {'✅Завершено' if self.mark else '⏳ В процессе'}\n"
            f"✨ Оценка: {self.mark if self.mark else '-'}/10\n"
        )

    def full_display(self) -> str:
        """Возвращает читаемое строковое представление задачи для пользователя (id не включается)"""
        # Эмодзи для типа задачи
        type_emoji = "🎤" if self.solution.task.type == TaskType.WRITING else "📝"

        # Статус выполнения
        status = "✅ Завершено" if self.mark is not None else "⏳ В процессе"

        # Оценка в виде звезд
        rating = self.mark if self.mark is not None else "-" + "/10"

        # Формируем текст
        return (
            f"{type_emoji}  {self.solution.task.title}\n"
            f"📅 Дата: {self.solution.created_at}\n"
            f"🔄 Статус: {status}\n"
            f"✨ Оценка: {rating}\n"
            f"📝 Ответ:\n{self.solution.content}"
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
