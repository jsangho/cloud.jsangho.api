from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WalterRoasterQuery:
    """WalterRoasterSchema 조회용 DTO."""

    id: int
    name: str
    memo: str
