"""crew_walter_roaster 도메인 엔티티."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WalterRoasterEntity:
    id: int
    name: str
    memo: str
