from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from database import LAYER_LOG
from titanic.app.use_cases.passenger_service import PassengerService

logger = LAYER_LOG


class TitanicQueryImpl:
    """타이타닉 조회 유스케이스."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self._passenger_service = PassengerService(db)

    def get_problem_summary(self) -> str:
        return self._passenger_service.get_problem_summary()

    async def get_data(self) -> list[dict]:
        logger.info("[TitanicQueryImpl] get_data -> PassengerService")
        return await self._passenger_service.get_data()

    async def get_count(self) -> int:
        return await self._passenger_service.get_count()

    async def get_survived_count(self) -> int:
        return await self._passenger_service.get_survived_count()

    async def get_dead_count(self) -> int:
        return await self._passenger_service.get_dead_count()

    def get_model_name(self) -> str:
        logger.info("[TitanicQueryImpl] get_model_name -> PassengerService")
        return self._passenger_service.get_model_name()

    def has_decision_tree_model(self) -> bool:
        return self._passenger_service.has_decision_tree_model()
