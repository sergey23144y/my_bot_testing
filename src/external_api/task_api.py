from faker import Faker
from src.schemas.Task.task_model import TaskModel, TaskListModel


fake = Faker("ru_RU")

MOCK_TOTAL = 40


def generate_mock_task(task_id: int, number_task: int) -> TaskModel:
    return TaskModel(
        id=task_id,
        title=fake.sentence(nb_words=3),
        description=fake.text(max_nb_chars=100),
        number_task=number_task,
        author=fake.name(),
    )


def get_list_task(
    page: int,
    number_task: int,
    limit_page: int = 5,
) -> TaskListModel:
    task_list: list[TaskModel] = []
    for i in range(page * limit_page, (page + 1) * limit_page):
        task_list.append(generate_mock_task(i + 1, number_task))
    return TaskListModel(tasks=task_list, total=MOCK_TOTAL)


def get_task_by_id(
    task_id: int,
    number_task: int,
) -> TaskModel:
    return generate_mock_task(task_id, number_task)
