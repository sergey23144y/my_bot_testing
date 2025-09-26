from pydantic import BaseModel


class TaskPDO(BaseModel):
    id: int
    title: str
    description: str
    number_task: int
    author: str


def format_task(task: TaskPDO) -> str:
    return (
        f"🆔 Задача #{task.id} (Номер задания: {task.number_task})\n"
        f"📝 Название : {task.title}\n"
        f"📖 Описание : {task.description}\n"
        f"👤 Автор: {task.author}"
    )
