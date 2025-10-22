from enum import Enum
import json


class NumberTask(Enum):
    TASK_37 = ("37", "37 – Личное письмо")
    TASK_38 = ("38", "38 – Диаграмма с комментарием")
    TASK_39 = ("39", "39 – Эссе")

    def __init__(self, number, description):
        self.number = number
        self.description = description

        # 🔹 сериализация

    def to_json(self):
        return json.dumps(
            {"name": self.name, "number": self.number, "description": self.description}
        )

    # 🔹 десериализация
    @classmethod
    def from_json(cls, data: str):
        obj = json.loads(data)
        return cls[obj["name"]]


class TaskType(Enum):
    WRITING = "writing"
    SPEAKING = "speaking"
