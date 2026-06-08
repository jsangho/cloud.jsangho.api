"""passenger_cal_tester 도메인 엔티티."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CalTesterEntity:
    id: int
    name: str
    memo: str
