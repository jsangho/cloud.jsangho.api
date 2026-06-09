from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse


class CalTesterUseCase(ABC):
    """`/titanic/cal/*` inbound(cal_tester_router) 입력 포트."""

    @abstractmethod
    async def introduce_myself(self, query: CalTesterQuery) -> CalTesterResponse:
        """캘던 하클리의 자기소개 메소드 (`GET /myself`)."""
        ...
