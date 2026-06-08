"""crew_lowe_boat 값 객체."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LoweBoatVo:
    id: int
    name: str
    memo: str
