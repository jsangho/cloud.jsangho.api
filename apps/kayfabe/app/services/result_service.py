from __future__ import annotations

from database import LAYER_LOG
from kayfabe.app.repositories.result_repository import ResultRepository
from kayfabe.app.schemas.result_schema import PleResultsResponse, PleResultRow

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
