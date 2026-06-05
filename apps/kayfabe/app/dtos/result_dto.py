from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from kayfabe.adapter.inbound.api.schemas.result_schema import PleResultRow, PleResultsResponse

PleEventStatus = Literal["upcoming", "live", "finished"]


@dataclass(frozen=True)
class PleResultRowDto:
    slug: str
    label: str
    month: int
    year: int
    event_at: datetime | None
    status: PleEventStatus
    finished_at: datetime | None

    def to_schema(self):
        from kayfabe.adapter.inbound.api.schemas.result_schema import PleResultRow

        return PleResultRow(
            slug=self.slug,
            label=self.label,
            month=self.month,
            year=self.year,
            eventAt=self.event_at,
            status=self.status,
            finishedAt=self.finished_at,
        )


@dataclass(frozen=True)
class PleResultsDto:
    year: int
    results: list[PleResultRowDto]

    def to_schema(self):
        from kayfabe.adapter.inbound.api.schemas.result_schema import PleResultsResponse

        return PleResultsResponse(year=self.year, results=[r.to_schema() for r in self.results])

