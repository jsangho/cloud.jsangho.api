"""crew_lowe_boat 도메인 엔티티."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LoweBoatEntity:
    id: int
    name: str
    memo: str
