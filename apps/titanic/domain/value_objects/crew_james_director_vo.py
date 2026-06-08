"""crew_james_director 값 객체."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JamesDirectorVo:
    id: int
    name: str
    memo: str
