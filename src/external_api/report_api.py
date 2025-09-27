from faker import Faker
from src.external_api.task_api import generate_mock_task
from src.schemas.Report.report_model import ReportModel, ReportListModel
import random

fake = Faker("ru_RU")

MOCK_TOTAL = 40


def generate_mock_report(report_id: int, number_task: int) -> ReportModel:
    return ReportModel(
        id=report_id,
        answer=fake.text(max_nb_chars=100),
        task=generate_mock_task(report_id, number_task),
        score=random.randint(1, 5),
    )


def get_list_report(
    page: int,
    number_task: int,
    limit_page: int = 5,
) -> ReportListModel:
    reports_list: list[ReportModel] = []
    for i in range(page * limit_page, (page + 1) * limit_page):
        reports_list.append(generate_mock_report(i + 1, number_task))
    return ReportListModel(reports=reports_list, total=MOCK_TOTAL)


def get_report_by_id(
    report_id: int,
    number_task: int,
) -> ReportModel:
    return generate_mock_report(report_id, number_task)
