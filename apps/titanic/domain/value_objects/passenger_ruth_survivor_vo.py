"""passenger_ruth_survivor 값 객체."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuthSurvivorVo:
    id: int
    name: str
    memo: str
