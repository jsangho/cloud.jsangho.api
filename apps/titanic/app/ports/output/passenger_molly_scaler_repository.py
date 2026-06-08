from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class MollyScalerRepository(ABC):
    """Cal 권총 조회 데이터 출력 포트."""

    @abstractmethod
    async def get_scaler(self) -> dict[str, Any]:
        ...
