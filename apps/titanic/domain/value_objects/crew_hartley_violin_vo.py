"""crew_hartley_violin 값 객체."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HartleyViolinVo:
    id: int
    name: str
    memo: str
