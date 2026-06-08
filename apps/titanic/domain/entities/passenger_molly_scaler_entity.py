"""passenger_molly_scaler 도메인 엔티티."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MollyScalerEntity:
    id: int
    name: str
    memo: str
