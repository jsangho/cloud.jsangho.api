from __future__ import annotations

from core.matrix.grid_oracle_database_manager import LAYER_LOG
from kayfabe.adapter.inbound.api.schemas.result_schema import PleResultsResponse
from kayfabe.app.dtos.result_dto import PleResultRowDto, PleResultsDto
from kayfabe.app.ports.input.result_use_case import ResultUseCase
from kayfabe.app.ports.output.result_repository import ResultRepository

logger = LAYER_LOG


class ResultInteractor(ResultUseCase):
    def __init__(self, repository: ResultRepository) -> None:
        self._repository = repository

    async def list_results(self, year: int) -> PleResultsResponse:
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
        return PleResultsDto(year=year, results=rows).to_schema()
