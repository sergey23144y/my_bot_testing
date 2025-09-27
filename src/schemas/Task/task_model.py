from typing import List, Optional
from pydantic import BaseModel


class TaskModel(BaseModel):
    id: int
    title: str
    description: str
    number_task: int
    author: str

    def __str__(self) -> str:
        """Возвращает читаемое строковое представление задачи"""
        return (
            f"🆔 Задача #{self.id} (Номер задания: {self.number_task})\n"
            f"📝 Название: {self.title}\n"
            f"📖 Описание: {self.description}\n"
            f"👤 Автор: {self.author}"
        )


class TaskListModel(BaseModel):
    tasks: List[TaskModel]
    total: int

    def get_by_id(self, task_id: int) -> Optional[TaskModel]:
        """Получить задачу по id"""
        return next((task for task in self.tasks if task.id == task_id), None)

    def get_by_number_task(self, number_task: int) -> List[TaskModel]:
        """Получить все задачи конкретного варианта"""
        return [task for task in self.tasks if task.number_task == number_task]

    def paginate(
        self, number_task: int, page: int, page_size: int = 5
    ) -> List[TaskModel]:
        """Вернуть задачи с пагинацией"""
        filtered = self.get_by_number_task(number_task)
        start = page * page_size
        end = start + page_size
        return filtered[start:end]

    def get_total(self) -> int:
        return self.total

    def __str__(self) -> str:
        return "\n\n".join(str(task) for task in self.tasks)
