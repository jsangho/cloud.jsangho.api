from __future__ import annotations

import logging

from kayfabe.app.dtos.result_dto import PleResultRowDto, PleResultsDto
from kayfabe.app.ports.input.result_use_case import ResultUseCase
from kayfabe.app.ports.output.result_repository import ResultRepository

logger = logging.getLogger("uvicorn.error")


class ResultInteractor(ResultUseCase):
    def __init__(self, repository: ResultRepository) -> None:
        self._repository = repository

    async def list_results(self, year: int) -> PleResultsDto:
        logger.info("[ResultInteractor] list_results | year=%d", year)
        events = await self._repository.list_events_by_year(year)
        rows: list[PleResultRowDto] = [
            PleResultRowDto(
                slug=ple.slug,
                label=ple.label,
                month=ple.month,
                year=ple.year,
                event_at=ple.finished_at,
                status=ple.status,  # type: ignore[arg-type]
                finished_at=ple.finished_at,
            )
            for ple in events
        ]
        return PleResultsDto(year=year, results=rows)
