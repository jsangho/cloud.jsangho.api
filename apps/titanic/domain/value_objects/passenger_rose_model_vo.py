"""passenger_rose_model 값 객체."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RoseModelVo:
    id: int
    name: str
    memo: str
