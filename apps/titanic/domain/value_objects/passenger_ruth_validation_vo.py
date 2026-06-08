"""passenger_ruth_validation 값 객체."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuthValidationVo:
    id: int
    name: str
    memo: str
