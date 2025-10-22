from aiogram import Router
from src.handlers import (
    examples,
    pricing,
    rewriter,
    support,
    written_part,
    oral_part,
    reports,
    start,
)

list_router = [
    start.start_router,
    examples.examples_router,
    pricing.pricing_router,
    rewriter.rewriter_router,
    support.support_router,
    written_part.written_router,
    # oral_part.oral_router,
    reports.reports_router,
]

routers = Router()

for item in list_router:
    routers.include_router(item)
