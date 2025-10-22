from faker import Faker
from src.external_api.dependencies.mock_task import generate_mock_task
from src.schemas.Report.report_model import ReportModel, ReportListModel, SolutionModal
import random

fake = Faker("ru_RU")

MOCK_TOTAL = 40


def generate_mock_solution(report_id: int) -> SolutionModal:
    return SolutionModal(
        id=report_id,
        content=fake.text(max_nb_chars=100),
        created_at=fake.date(pattern="%d.%m.%Y"),
    )


def generate_mock_report(report_id: int) -> ReportModel:
    return ReportModel(
        id=report_id,
        solution=generate_mock_solution(report_id),
        task=generate_mock_task(report_id),
        mark=random.randint(0, 5),
        analysis=fake.text(max_nb_chars=100),
    )


def get_list_report(
    page: int,
    limit_page: int = 5,
) -> ReportListModel:
    reports_list: list[ReportModel] = []
    for i in range(page * limit_page, (page + 1) * limit_page):
        reports_list.append(generate_mock_report(i + 1))
    return ReportListModel(reports=reports_list, total=MOCK_TOTAL)


def get_report_by_id(
    report_id: int,
) -> ReportModel:
    return generate_mock_report(report_id)
