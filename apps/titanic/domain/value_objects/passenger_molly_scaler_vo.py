"""passenger_molly_scaler 값 객체."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MollyScalerVo:
    id: int
    name: str
    memo: str
