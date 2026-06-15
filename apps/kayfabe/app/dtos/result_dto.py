from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from kayfabe.adapter.inbound.api.schemas.ple_events_schema import PleResultRowSchema, PleResultsResponseSchema

PleEventStatus = Literal["upcoming", "live", "finished"]


@dataclass(frozen=True)
class PleResultRowResponse:
    slug: str
    label: str
    month: int
    year: int
    event_at: datetime | None
    status: PleEventStatus
    finished_at: datetime | None

    def to_schema(self):
        from kayfabe.adapter.inbound.api.schemas.ple_events_schema import PleResultRowSchema

        return PleResultRowSchema(
            slug=self.slug,
            label=self.label,
            month=self.month,
            year=self.year,
            eventAt=self.event_at,
            status=self.status,
            finishedAt=self.finished_at,
        )


@dataclass(frozen=True)
class PleResultsResponse:
    year: int
    results: list[PleResultRowResponse]

    def to_schema(self):
        from kayfabe.adapter.inbound.api.schemas.ple_events_schema import PleResultsResponseSchema

        return PleResultsResponseSchema(year=self.year, results=[r.to_schema() for r in self.results])
