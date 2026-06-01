from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IsidorBedUseCase(ABC):
    """`/titanic/isidor/*` inbound(isidor_bed_router) 입력 포트."""

    @abstractmethod
    async def get_bed(self) -> dict[str, Any]:
        """침대 조회 (`GET /bed`)."""
        ...
