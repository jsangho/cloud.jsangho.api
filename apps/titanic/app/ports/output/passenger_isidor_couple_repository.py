from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IsidorCoupleRepository(ABC):
    """Isidor 침대 조회 데이터 출력 포트."""

    @abstractmethod
    async def get_couple(self) -> dict[str, Any]:
        ...
