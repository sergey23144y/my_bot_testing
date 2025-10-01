from typing import List, Optional
from pydantic import BaseModel

from src.schemas.Task.task_model import TaskModel
from src.utils.digit_emojis import rating_stars


class ReportModel(BaseModel):
    id: int
    task: TaskModel
    score: int

    def __str__(self) -> str:
        """Возвращает читаемое строковое представление задачи"""
        return (
            f"🆔 Задача #{self.task.id} (Номер задания: {self.task.number_task})\n"
            f"📝 Название задачи: {self.task.title}\n"
            f"✨ Оценка: {rating_stars(self.score)}\n"
        )


class ReportWrittenModel(BaseModel):
    answer: str

    def full_display(self):
        """Возвращает читаемое строковое представление задачи"""
        return (
            f"🆔 Задача #{self.task.id} (Номер задания: {self.task.number_task})\n"
            f"📝 Название задачи: {self.task.title}\n"
            f"✨ Оценка: {rating_stars(self.score)}\n"
            f"📝 Ответ: {self.answer}\n"
        )


class ReportOralModel(BaseModel):
    answer_filename: str

    def full_display(self):
        """Возвращает читаемое строковое представление задачи"""
        return (
            f"🆔 Задача #{self.task.id} (Номер задания: {self.task.number_task})\n"
            f"📝 Название задачи: {self.task.title}\n"
            f"✨ Оценка: {rating_stars(self.score)}\n"
            f"📝 Ответ: {self.answer_filename}\n"
        )


class ReportListModel(BaseModel):
    reports: List[ReportModel]
    total: int

    def get_by_id(self, report_id: int) -> Optional[ReportModel]:
        """Получить задачу по id"""
        return next((report for report in self.reports if report.id == report_id), None)

    def get_total(self) -> int:
        return self.total

    def __str__(self) -> str:
        return "\n\n".join(str(report) for report in self.reports)
