from __future__ import annotations

from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.output.passenger_cal_tester_repository import CalTesterRepository

class CalTesterInteractor(CalTesterUseCase):

    def __init__(self, repository: CalTesterRepository):
        self.repository = repository

    async def introduce_myself(self, query: CalTesterQuery) -> CalTesterResponse:
        return await self.repository.introduce_myself(query)
