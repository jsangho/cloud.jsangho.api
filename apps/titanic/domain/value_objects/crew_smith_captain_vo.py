"""crew_smith_captain 값 객체."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SmithCaptainVo:
    id: int
    name: str
    memo: str
