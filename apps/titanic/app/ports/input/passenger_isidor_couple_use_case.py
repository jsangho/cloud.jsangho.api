from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IsidorCoupleUseCase(ABC):
    """`/titanic/isidor/*` inbound(isidor_couple_router) 입력 포트."""

    @abstractmethod
    async def get_couple(self) -> dict[str, Any]:
        """침대 조회 (`GET /bed`)."""
        ...
