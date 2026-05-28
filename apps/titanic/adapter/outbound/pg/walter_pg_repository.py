from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LAYER_LOG
from titanic.app.use_cases.titanic_models import PassengerModel

logger = LAYER_LOG


class WalterPgRepository:
    """Neon(Postgres) 조회 어댑터."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def list_page(self, *, page: int, page_size: int) -> dict:
        safe_page_size = max(1, min(int(page_size), 200))
        safe_page = max(1, int(page))
        offset = (safe_page - 1) * safe_page_size

        logger.info(
            "[WalterOpenFile] pg_adapter read from neon page=%s page_size=%s",
            safe_page,
            safe_page_size,
        )

        count_result = await self._db.execute(select(func.count()).select_from(PassengerModel))
        total = int(count_result.scalar_one())

        result = await self._db.execute(
            select(PassengerModel)
            .order_by(PassengerModel.passenger_id.asc())
            .offset(offset)
            .limit(safe_page_size)
        )
        rows = result.scalars().all()

        items = [
            {
                "PassengerId": r.passenger_id,
                "Survived": r.survived,
                "Pclass": r.pclass,
                "Name": r.name,
                "gender": r.sex,
                "Age": r.age,
                "SibSp": r.sibsp,
                "Parch": r.parch,
                "Ticket": r.ticket,
                "Fare": r.fare,
                "Cabin": r.cabin,
                "Embarked": r.embarked,
            }
            for r in rows
        ]

        return {
            "page": safe_page,
            "pageSize": safe_page_size,
            "total": total,
            "items": items,
        }
