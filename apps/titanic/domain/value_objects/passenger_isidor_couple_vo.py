"""passenger_isidor_couple 값 객체."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IsidorCoupleVo:
    id: int
    name: str
    memo: str
