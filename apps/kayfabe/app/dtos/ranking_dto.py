from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LeaderboardRow:
    rank: int
    nickname: str
    score: int
    correct: int
    graded: int


@dataclass(frozen=True)
class RankingRowDto:
    rank: int
    nickname: str
    score: int
    accuracy: float


@dataclass(frozen=True)
class RankingsDto:
    rows: list[RankingRowDto]
    my_rank: RankingRowDto | None
