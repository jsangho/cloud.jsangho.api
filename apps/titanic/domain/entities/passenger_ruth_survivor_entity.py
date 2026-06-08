"""passenger_ruth_survivor 도메인 엔티티."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RuthSurvivorEntity:
    id: int
    name: str
    memo: str
