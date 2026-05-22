from __future__ import annotations

from database import LAYER_LOG
from kayfabe.app.repositories.result_repository import ResultRepository
from kayfabe.app.schemas.result_schema import PleResultsResponse, PleResultRow

logger = LAYER_LOG


class ResultService:
    def __init__(self, repo: ResultRepository) -> None:
        self.repo = repo

    async def list_results(self, year: int) -> PleResultsResponse:
        pairs = await self.repo.list_results(year)
        rows: list[PleResultRow] = []
        for ple, result in pairs:
            status = result.status if result else ple.status
            finished_at = result.finished_at if result else ple.finished_at
            rows.append(
                PleResultRow(
                    slug=ple.slug,
                    label=ple.label,
                    month=ple.month,
                    year=ple.year,
                    eventAt=finished_at,
                    status=status,  # type: ignore[arg-type]
                    finishedAt=finished_at,
                )
            )
        return PleResultsResponse(year=year, results=rows)