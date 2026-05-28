from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LAYER_LOG
from titanic.app.schemas.passenger_schema import PassengerSchema
from titanic.app.schemas.problem_definition import PROBLEM_SUMMARY
from titanic.app.use_cases.reader_use_case import PassengerRepository
from titanic.app.use_cases.titanic_models import SurvivalModel
from titanic.app.use_cases.validation_use_case import (
    validate_feature_columns,
    validate_passenger_schema,
)

logger = LAYER_LOG


class PassengerService:
    def __init__(self, db: AsyncSession | None = None) -> None:
        self.passenger_repository = PassengerRepository(db)
        self.survival_model = SurvivalModel()

    def get_problem_summary(self) -> str:
        return PROBLEM_SUMMARY

    async def get_data(self) -> list[dict]:
        logger.info("[PassengerService] get_data -> Repository (Neon)")
        row = await self.passenger_repository.get_sample_row_in_neon()
        return [row] if row else []

    async def get_count(self) -> int:
        return await self.passenger_repository.count_in_neon()

    async def get_survived_count(self) -> int:
        return await self.passenger_repository.survived_count_in_neon()

    async def get_dead_count(self) -> int:
        return await self.passenger_repository.dead_count_in_neon()

    def get_model_name(self) -> str:
        return self.survival_model.get_model_name()

    def has_decision_tree_model(self) -> bool:
        return self.survival_model.is_ready

    def validate_dataset_columns(self) -> list[str]:
        return validate_feature_columns(list(PassengerSchema.model_fields.keys()))

    async def save_passenger(self, passenger: PassengerSchema) -> None:
        errors = validate_passenger_schema(passenger)
        if errors:
            raise HTTPException(status_code=400, detail="; ".join(errors))

        column_errors = self.validate_dataset_columns()
        if column_errors:
            raise HTTPException(status_code=400, detail="; ".join(column_errors))

        logger.info(
            "[PassengerService] save_passenger -> Repository — passengerId=%s",
            passenger.PassengerId,
        )
        await self.passenger_repository.save_passenger(passenger)
        logger.info(
            "[PassengerService] save_passenger <- Repository — passengerId=%s",
            passenger.PassengerId,
        )
