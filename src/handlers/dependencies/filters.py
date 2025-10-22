import logging
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from typing import Optional
from src.core.enums import NumberTask

logger = logging.getLogger(__name__)


class NumberTaskFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> Optional[dict]:
        """
        Возвращает dict с 'task' (объект Enum), если callback_data совпадает.
        Если совпадений нет — фильтр не срабатывает.
        """
        for number in NumberTask:
            logger.info(callback.data)
            if callback.data == number.number or callback.data == number.number[0]:
                return {"number": number}
        return False
