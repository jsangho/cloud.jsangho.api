from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.adapter.inbound.api.schemas.result_schema import PleResultsResponse


class ResultUseCase(ABC):
    """`/ple/results/results` inbound(result_router)가 호출하는 입력 포트."""

    @abstractmethod
    async def list_results(self, year: int) -> PleResultsResponse:
        """연도별 PLE 이벤트 결과 목록."""
        ...
