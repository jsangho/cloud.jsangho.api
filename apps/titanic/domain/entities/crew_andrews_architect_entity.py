"""crew_andrews_architect 도메인 엔티티."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AndrewsArchitectEntity:
    id: int
    name: str
    memo: str
