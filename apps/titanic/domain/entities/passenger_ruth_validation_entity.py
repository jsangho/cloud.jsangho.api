"""passenger_ruth_validation 도메인 엔티티."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RuthValidationEntity:
    id: int
    name: str
    memo: str
