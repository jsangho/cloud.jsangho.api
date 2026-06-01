from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IsidorBedRepository(ABC):
    """Isidor 침대 조회 데이터 출력 포트."""

    @abstractmethod
    async def get_bed(self) -> dict[str, Any]:
        ...
