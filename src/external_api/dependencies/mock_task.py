from faker import Faker
from src.schemas.Task.task_model import TaskModel, TaskListModel
from src.core.enums import NumberTask, TaskType
from random import choice

fake = Faker("ru_RU")

MOCK_TOTAL = 40


def generate_mock_task(
    task_id: int, number: NumberTask | None = None, type: TaskType | None = None
) -> TaskModel:
    return TaskModel(
        id=task_id,
        title=fake.sentence(nb_words=3),
        content=fake.text(max_nb_chars=100),
        number=number if number else choice(list(NumberTask)),
        type=type if type else choice(list(TaskType)),
    )


def get_list_task(
    page: int,
    number: NumberTask | None = None,
    type: TaskType | None = None,
    limit_page: int = 5,
) -> TaskListModel:
    task_list: list[TaskModel] = []
    for i in range(page * limit_page, (page + 1) * limit_page):
        task_list.append(generate_mock_task(i + 1, number, type))
    return TaskListModel(tasks=task_list, total=MOCK_TOTAL)


def get_task_by_id(
    task_id: int,
    number: NumberTask,
    type: TaskType | None = None,
) -> TaskModel:
    return generate_mock_task(task_id, number, type)
