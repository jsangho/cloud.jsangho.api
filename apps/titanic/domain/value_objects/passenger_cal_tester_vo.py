"""passenger_cal_tester 값 객체."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CalTesterVo:
    id: int
    name: str
    memo: str
