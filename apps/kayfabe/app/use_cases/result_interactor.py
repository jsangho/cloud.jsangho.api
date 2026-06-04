from __future__ import annotations

from core.matrix.oracle_database import LAYER_LOG
from kayfabe.adapter.outbound.pg.result_pg_repository import ResultRepository
from kayfabe.app.ports.input.result_schema import PleResultRow, PleResultsResponse

logger = LAYER_LOG


class ResultService:
    def __init__(self, repo: ResultRepository) -> None:
        self.repo = repo

    async def list_results(self, year: int) -> PleResultsResponse:
        events = await self.repo.list_events_by_year(year)
        rows: list[PleResultRow] = []
        for ple in events:
            rows.append(
                PleResultRow(
                    slug=ple.slug,
                    label=ple.label,
                    month=ple.month,
                    year=ple.year,
                    eventAt=ple.finished_at,
                    status=ple.status,  # type: ignore[arg-type]
                    finishedAt=ple.finished_at,
                )
            )
        return PleResultsResponse(year=year, results=rows)

