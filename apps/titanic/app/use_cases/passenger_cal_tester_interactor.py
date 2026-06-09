from __future__ import annotations

import logging

from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.output.passenger_cal_tester_repository import CalTesterRepository

logger = logging.getLogger("uvicorn.error")


class CalTesterInteractor(CalTesterUseCase):

    def __init__(self, repository: CalTesterRepository):
        self.repository = repository

    async def introduce_myself(self, query: CalTesterQuery) -> CalTesterResponse:
        logger.info("[CalTesterUseCase] introduce_myself | request_data=%s", f"id={query.id} name={query.name!r}")
        return await self.repository.introduce_myself(query)
