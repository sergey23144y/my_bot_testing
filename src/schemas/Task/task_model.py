import json
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from src.core.enums import NumberTask, TaskType


class TaskModel(BaseModel):
    id: int
    title: str
    content: str
    type: TaskType
    number: NumberTask
    image_url: Optional[str] = None
    last_solution_mark: Optional[int] = None
    created_at: str = Field(alias="created_at")
    updated_at: str = Field(alias="updated_at")

    class Config:
        fields = {
            "created_at": "createdAt",
            "updated_at": "updatedAt",
        }

    @field_validator("number", mode="before")
    @classmethod
    def validate_number(cls, v):
        if isinstance(v, str):
            # ищем Enum по number
            for item in NumberTask:
                if item.number == v:
                    return item
        return v

    def to_string(self, IsPrintContent: bool = False) -> str:
        """Возвращает читаемое строковое представление задачи"""
        text = (
            f"🆔 Задача #{self.id}\n"
            f"📝 Название: {self.title}\n"
            f"📖 Последняя оценка: {self.last_solution_mark + '/10' if self.last_solution_mark else '-'}\n"
        )

        if IsPrintContent:
            text += f"📝 Текст задачи: {self.content}\n"
        return text

    def to_json(self) -> str:
        """Возвращает JSON-представление задачи"""
        data = {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "type": self.type.value,  # Enum → строка
            "number": self.number.to_json(),  # Enum → "37"
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "TaskModel":
        """Десериализация задачи из JSON"""
        return cls.model_validate_json(json_str)


class MetaModel(BaseModel):
    total_items: int = Field(alias="totalItems")
    item_count: int = Field(alias="itemCount")
    items_per_page: int = Field(alias="itemsPerPage")
    total_pages: int = Field(alias="totalPages")
    current_page: int = Field(alias="currentPage")


class TaskListModel(BaseModel):
    tasks: List[TaskModel] = Field(alias="data")
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

    def to_string(self) -> str:
        return "\n\n".join(task.to_string() for task in self.tasks)
