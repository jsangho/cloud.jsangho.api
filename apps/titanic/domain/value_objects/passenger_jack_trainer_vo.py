"""passenger_jack_trainer 값 객체."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JackTrainerVo:
    id: int
    name: str
    memo: str
