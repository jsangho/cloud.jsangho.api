"""crew_hartley_violin 도메인 엔티티."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HartleyViolinEntity:
    id: int
    name: str
    memo: str
