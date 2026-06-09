from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal


@dataclass(frozen=True)
class CompetitorDto:
    name: str
    is_champion: bool | None = None


@dataclass(frozen=True)
class MatchResultDto:
    winner_side: Literal["left", "right"] | None = None
    winner_index: int | None = None
    winner_name: str | None = None


@dataclass(frozen=True)
class MatchCardSyncCommand:
    id: str
    title: str
    card_variant: Literal["sideA", "sideB"]
    format: Literal["singles", "multi"]
    left: CompetitorDto | None = None
    right: CompetitorDto | None = None
    competitors: list[CompetitorDto] | None = None
    bookmaker_decimal: dict[str, Any] | list[float] | None = None
    result: MatchResultDto | None = None


@dataclass(frozen=True)
class PleEventSyncCommand:
    slug: str
    label: str
    month: int
    year: int
    status: Literal["upcoming", "live", "finished"] | None
    matches: list[MatchCardSyncCommand]


@dataclass(frozen=True)
class PredictionCommand:
    pick: str
    client_id: str
    user_id: int


@dataclass(frozen=True)
class PredictionItemCommand:
    match_key: str
    pick: str


@dataclass(frozen=True)
class BatchPredictionCommand:
    client_id: str
    user_id: int
    predictions: list[PredictionItemCommand]


@dataclass(frozen=True)
class BatchResultItemCommand:
    match_key: str
    winner_side: Literal["left", "right"] | None = None
    winner_index: int | None = None
    winner_name: str | None = None
    status: Literal["scheduled", "live", "finished"] | None = "finished"


@dataclass(frozen=True)
class BatchResultsCommand:
    results: list[BatchResultItemCommand]


@dataclass(frozen=True)
class MatchResultUpdateCommand:
    winner_side: Literal["left", "right"] | None = None
    winner_index: int | None = None
    winner_name: str | None = None
    status: Literal["scheduled", "live", "finished"] | None = None


@dataclass(frozen=True)
class VoteTotalsDto:
    left: int = 0
    right: int = 0
    multi: list[int] = field(default_factory=list)


@dataclass(frozen=True)
class MatchBoardDto:
    id: str
    db_id: int
    title: str
    card_variant: str
    format: Literal["singles", "multi"]
    left: CompetitorDto | None
    right: CompetitorDto | None
    competitors: list[CompetitorDto] | None
    bookmaker_decimal: dict[str, Any] | list[float] | None
    status: str
    result: MatchResultDto | None
    site_votes: VoteTotalsDto
    locked: bool
    my_pick: str | None
    ai_pick: str | None
    ai_pick_name: str | None
    ai_correct: bool | None


@dataclass(frozen=True)
class PleBoardDto:
    slug: str
    label: str
    month: int
    year: int
    status: str
    finished_at: datetime | None
    matches: list[MatchBoardDto]
    updated_at: datetime


@dataclass(frozen=True)
class PleAiRecordDto:
    event_slug: str
    event_label: str
    match_key: str
    match_title: str
    ai_pick_name: str
    winner_name: str | None
    correct: bool


@dataclass(frozen=True)
class PleAiStatsDto:
    total_graded: int
    correct: int
    incorrect: int
    accuracy_percent: float | None
    recent: list[PleAiRecordDto]


@dataclass(frozen=True)
class PleEventSummaryDto:
    slug: str
    label: str
    month: int
    year: int
    status: str
    match_count: int


@dataclass(frozen=True)
class PleMatchSnapshotDto:
    id: int
    match_key: str
    status: str


@dataclass(frozen=True)
class PleEventSnapshotDto:
    id: int
    slug: str
    status: str
    finished_at: datetime | None
    matches: list[PleMatchSnapshotDto]


@dataclass(frozen=True)
class PleMatchReadDto:
    id: int
    match_key: str
    title: str
    format: Literal["singles", "multi"]
    card_variant: str
    sort_order: int
    card_json: str
    status: str
    winner_pick: str | None
    winner_name: str | None
    ai_pick: str | None
    ai_pick_name: str | None
    ai_correct: bool | None


@dataclass(frozen=True)
class PleEventReadDto:
    slug: str
    label: str
    month: int
    year: int
    status: str
    finished_at: datetime | None
    updated_at: datetime
    matches: list[PleMatchReadDto]
