from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ChampionshipTier = Literal["main", "secondary", "tag", "other"]
BrandId = Literal["raw", "smackdown", "nxt", "global"]
BrandAccent = Literal["red", "blue", "gold", "purple"]


@dataclass(frozen=True)
class TitleReignDto:
    belt_name: str
    champions: list[str]
    won_at: str
    tier: ChampionshipTier
    team_name: str | None = None
    won_event: str | None = None

    def to_schema(self):
        from kayfabe.adapter.inbound.api.schemas.championship_schema import TitleReignSchema

        return TitleReignSchema(
            belt_name=self.belt_name,
            champions=list(self.champions),
            team_name=self.team_name,
            won_at=self.won_at,
            won_event=self.won_event,
            tier=self.tier,
        )


@dataclass(frozen=True)
class BrandRosterDto:
    id: BrandId
    label: str
    tagline: str
    accent: BrandAccent
    titles: list[TitleReignDto]

    def to_schema(self):
        from kayfabe.adapter.inbound.api.schemas.championship_schema import BrandRosterSchema

        return BrandRosterSchema(
            id=self.id,
            label=self.label,
            tagline=self.tagline,
            accent=self.accent,
            titles=[t.to_schema() for t in self.titles],
        )


@dataclass(frozen=True)
class ChampionshipBoardDto:
    as_of: str
    brands: list[BrandRosterDto]

    def to_schema(self):
        from kayfabe.adapter.inbound.api.schemas.championship_schema import (
            ChampionshipBoardResponseSchema,
        )

        return ChampionshipBoardResponseSchema(
            as_of=self.as_of,
            brands=[b.to_schema() for b in self.brands],
        )
