from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import LAYER_LOG
from titanic.app.models.passenger_model import PassengerModel
from titanic.app.schemas.passenger_schema import PassengerSchema

logger = LAYER_LOG


class PassengerRepository:
    """Neon Postgres 접근 및 적재."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    async def get_sample_row_in_neon(self) -> dict | None:
        if self.db is None:
            return None
        result = await self.db.execute(
            select(PassengerModel).order_by(PassengerModel.passenger_id.asc()).limit(1)
        )
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return {
            "PassengerId": row.passenger_id,
            "Survived": row.survived,
            "Pclass": row.pclass,
            "Name": row.name,
            "Sex": row.sex,
            "Age": row.age,
            "SibSp": row.sibsp,
            "Parch": row.parch,
            "Ticket": row.ticket,
            "Fare": row.fare,
            "Cabin": row.cabin,
            "Embarked": row.embarked,
        }

    @staticmethod
    def schema_to_orm(passenger: PassengerSchema) -> PassengerModel:
        return PassengerModel(
            passenger_id=passenger.PassengerId or 0,
            survived=passenger.Survived,
            pclass=passenger.Pclass,
            name=passenger.Name,
            sex=passenger.Sex,
            age=passenger.Age,
            sibsp=passenger.SibSp,
            parch=passenger.Parch,
            ticket=passenger.Ticket,
            fare=passenger.Fare,
            cabin=passenger.Cabin,
            embarked=passenger.Embarked,
        )

    async def _flush_to_neon(self) -> None:
        if self.db is None:
            raise RuntimeError("Neon 세션이 필요합니다.")
        await self.db.flush()

    async def count_in_neon(self) -> int:
        if self.db is None:
            return 0
        result = await self.db.execute(select(func.count()).select_from(PassengerModel))
        return int(result.scalar_one())

    async def survived_count_in_neon(self) -> int:
        if self.db is None:
            return 0
        result = await self.db.execute(
            select(func.count()).select_from(PassengerModel).where(PassengerModel.survived == 1)
        )
        return int(result.scalar_one())

    async def dead_count_in_neon(self) -> int:
        if self.db is None:
            return 0
        result = await self.db.execute(
            select(func.count()).select_from(PassengerModel).where(PassengerModel.survived == 0)
        )
        return int(result.scalar_one())

    async def save_passenger(self, passenger: PassengerSchema) -> PassengerModel:
        if self.db is None:
            raise RuntimeError("Neon 세션이 필요합니다.")
        logger.info(
            "[PassengerRepository] save_passenger -> Neon — passengerId=%s",
            passenger.PassengerId,
        )
        row = self.schema_to_orm(passenger)
        self.db.add(row)
        await self._flush_to_neon()
        await self.db.refresh(row)
        logger.info(
            "[PassengerRepository] save_passenger <- Neon — passengerId=%s, db_id=%s",
            passenger.PassengerId,
            row.id,
        )
        return row
