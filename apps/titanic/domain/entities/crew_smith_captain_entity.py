"""crew_smith_captain 도메인 엔티티."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SmithCaptainEntity:
    id: int
    name: str
    memo: str
