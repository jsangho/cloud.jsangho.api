"""passenger_isidor_couple 도메인 엔티티."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class IsidorCoupleEntity:
    id: int
    name: str
    memo: str
