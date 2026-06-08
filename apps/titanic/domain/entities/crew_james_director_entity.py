"""crew_james_director 도메인 엔티티."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class JamesDirectorEntity:
    id: int
    name: str
    memo: str
