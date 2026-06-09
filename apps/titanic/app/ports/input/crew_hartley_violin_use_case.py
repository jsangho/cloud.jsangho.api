from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinQuery, HartleyViolinResponse


class HartleyViolinUseCase(ABC):
    """`/titanic/hartley/*` inbound(hartley_violin_router) 입력 포트."""

    @abstractmethod
    async def introduce_myself(self, query: HartleyViolinQuery) -> HartleyViolinResponse:
        """하틀리 자기소개 메소드 (`GET /myself`)."""
        ...
