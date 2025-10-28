import logging
from typing import Optional

from src.external_api.dependencies._make_request import _make_request
from src.external_api.http_client import http_client
from src.core.enums import NumberTask, TaskType
from src.schemas.Task.task_model import TaskModel, TaskListModel
from src.utils.redis_client import get_jwt_from_redis

logger = logging.getLogger(__name__)


async def fetch_list_task(
    page: int = 1,
    limit: int = 5,
    number: NumberTask | None = None,
    type: TaskType | None = None,
    telegram_id: int | None = None,
) -> Optional[TaskListModel]:
    return await _make_request(
        telegram_id=telegram_id,
        method="GET",
        endpoint="/tasks/writing/",
        model=TaskListModel,
        params={"page": page, "limit": limit, "number": number.number},
    )


async def fetch_task_by_id(
    task_id: int,
    telegram_id: int | None = None,
) -> Optional[TaskModel]:
    return await _make_request(
        telegram_id=telegram_id,
        method="GET",
        endpoint=f"/tasks/writing/{task_id}",
        model=TaskModel,
    )


async def send_solutions(telegram_id: int, task_id: int, content: str) -> bool:
    async with http_client as client:
        token = await get_jwt_from_redis(telegram_id)
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.post(
            f"/tasks/writing/{task_id}/solutions",
            json={"content": content},
            headers=headers,
        )
        if response.status_code != 201:
            return False
        return True
