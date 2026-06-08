"""crew_walter_roaster 값 객체."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WalterRoasterVo:
    id: int
    name: str
    memo: str
