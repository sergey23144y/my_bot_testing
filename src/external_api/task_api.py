from faker import Faker
from src.schemas.taskDTO import TaskPDO


fake = Faker("ru_RU")


def generate_mock_task(task_id: int, number_task: int) -> TaskPDO:
    return TaskPDO(
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
):
    task_list: list[TaskPDO] = []
    for i in range(page * limit_page, (page + 1) * limit_page):
        task_list.append(generate_mock_task(i + 1, number_task))
    return task_list


def get_task_by_id(
    task_id: int,
    number_task: int,
):
    return generate_mock_task(task_id, number_task)
