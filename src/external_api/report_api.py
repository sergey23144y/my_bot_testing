import logging
from typing import Optional

from src.external_api.dependencies._make_request import _make_request
from src.schemas.Report.report_model import ReportModel, ReportListModel

logger = logging.getLogger(__name__)


async def fetch_list_report(
    telegram_id: str,
    page: int = 1,
    limit: int = 5,
) -> Optional[ReportListModel]:
    return await _make_request(
        telegram_id=telegram_id,
        method="GET",
        endpoint="/reports",
        model=ReportListModel,
        params={"page": page, "limit": limit},
    )


async def fetch_report_by_id(
    telegram_id: str,
    report_id: int,
) -> Optional[ReportModel]:
    return await _make_request(
        telegram_id=telegram_id,
        method="GET",
        endpoint=f"/reports/{report_id}",
        model=ReportModel,
    )
