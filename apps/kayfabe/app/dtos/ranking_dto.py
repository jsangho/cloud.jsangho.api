from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LeaderboardRow:
    rank: int
    nickname: str
    score: int
    correct: int
    graded: int
