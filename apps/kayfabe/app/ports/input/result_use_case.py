from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.app.dtos.result_dto import PleResultsDto


class ResultUseCase(ABC):
    """`/ple/results/results` inbound(result_router) 입력 포트."""

    @abstractmethod
    async def list_results(self, year: int) -> PleResultsDto:
        """연도별 PLE 이벤트 결과 목록."""
        ...
