from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kayfabe.adapter.inbound.api.schemas.title_history_schema import (
        CompetitorTitleHistoryResponseSchema,
        TitleAcquisitionSchema,
    )


@dataclass(frozen=True)
class TitleAcquisitionDto:
    belt_name: str
    won_at: str
    won_at_slug: str | None
    match_key: str | None

    def to_schema(self):
        from kayfabe.adapter.inbound.api.schemas.title_history_schema import TitleAcquisitionSchema

        return TitleAcquisitionSchema(
            belt_name=self.belt_name,
            won_at=self.won_at,
            won_at_slug=self.won_at_slug,
            match_key=self.match_key,
        )


@dataclass(frozen=True)
class CompetitorTitleHistoryDto:
    name: str
    acquisitions: list[TitleAcquisitionDto]

    def to_schema(self):
        from kayfabe.adapter.inbound.api.schemas.title_history_schema import (
            CompetitorTitleHistoryResponseSchema,
        )

        items = [a.to_schema() for a in self.acquisitions]
        return CompetitorTitleHistoryResponseSchema(
            name=self.name,
            acquisitions=items,
            total=len(items),
        )
