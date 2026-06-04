from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import walter_roaster_open_info
from titanic.adapter.outbound.orm.booking_orm import BookingOrm
from titanic.adapter.outbound.orm.person_orm import PersonOrm
from titanic.app.dtos.walter_roaster_dto import WalterRoasterQuery
from titanic.app.ports.output.walter_roaster_repository import WalterRoasterRepository

logger = logging.getLogger("uvicorn.error")
_SRC = Path(__file__).name


class WalterRoasterPgRepository(WalterRoasterRepository):
    """PostgreSQL(Neon) `titanic_persons` + `titanic_bookings` 조회 저장소."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    def introduce_myself(self, query: WalterRoasterQuery, *, trace: bool = True) -> None:
        """승객 명단을 가져오는 메소드."""
        logger.info("########################################################################################")
        logger.info("🆗[월터 레포지토리] 유스케이스에서 가져온 월터 정보")
        logger.info("💌ID: %s", query.id)
        logger.info("👁‍🗨이름: %s", query.name)
        logger.info("📝비고: %s", query.memo)
        logger.info("########################################################################################")
        if trace:
            walter_roaster_open_info(_SRC, "-> repository")

    async def list_page(self, *, page: int, page_size: int) -> dict[str, Any]:
        safe_page_size = max(1, min(int(page_size), 200))
        safe_page = max(1, int(page))
        offset = (safe_page - 1) * safe_page_size

        count_result = await self._db.execute(
            select(func.count()).select_from(PersonOrm)
        )
        total = int(count_result.scalar_one())

        result = await self._db.execute(
            select(PersonOrm, BookingOrm)
            .join(BookingOrm, BookingOrm.person_id == PersonOrm.id)
            .order_by(PersonOrm.passenger_id.asc())
            .offset(offset)
            .limit(safe_page_size)
        )
        rows = result.all()

        items = [
            {
                "PassengerId": person.passenger_id,
                "Survived": person.survived,
                "Pclass": booking.pclass,
                "Name": person.name,
                "gender": person.gender,
                "Age": person.age,
                "SibSp": person.sib_sp,
                "Parch": person.parch,
                "Ticket": booking.ticket,
                "Fare": booking.fare,
                "Cabin": booking.cabin,
                "Embarked": booking.embarked,
            }
            for person, booking in rows
        ]

        walter_roaster_open_info(
            _SRC,
            "page=%s pageSize=%s total=%s -> Neon",
            safe_page,
            safe_page_size,
            total,
        )

        return {
            "page": safe_page,
            "pageSize": safe_page_size,
            "total": total,
            "items": items,
        }
