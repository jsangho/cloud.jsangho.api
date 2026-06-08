"""crew_andrews_architect 값 객체."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AndrewsArchitectVo:
    id: int
    name: str
    memo: str
