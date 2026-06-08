"""passenger_rose_model 도메인 엔티티."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RoseModelEntity:
    id: int
    name: str
    memo: str
