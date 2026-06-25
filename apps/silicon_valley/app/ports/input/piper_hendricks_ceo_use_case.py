from __future__ import annotations

from abc import ABC, abstractmethod

from silicon_valley.app.dtos.piper_hendricks_ceo_dto import (
    HendricksCeoQuery,
    HendricksCeoResponse,
)


class HendricksCeoUseCase(ABC):
    """`/silicon_valley/hendricks/*` inbound(hendricks_ceo_router) 입력 포트."""

    @abstractmethod
    async def introduce_myself(self, query: HendricksCeoQuery) -> HendricksCeoResponse:
        """리처드 헨드릭스의 자기소개 메소드 (`GET /myself`)."""
        ...
