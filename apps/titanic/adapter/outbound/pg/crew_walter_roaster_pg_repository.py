from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.booking_orm import BookingOrm
from titanic.adapter.outbound.orm.person_orm import PersonOrm
from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse
from titanic.app.ports.output.crew_walter_roaster_repository import WalterRoasterRepository
import logging

logger = logging.getLogger("uvicorn.error")


def _row_to_dict(person: PersonOrm, booking: BookingOrm | None) -> dict[str, Any]:
    return {
        "id": person.id,
        "passenger": person.passenger_id,
        "survived": person.survived,
        "pclass": booking.pclass if booking else None,
        "name": person.name,
        "gender": person.gender,
        "age": person.age,
        "sibsp": person.sib_sp,
        "parch": person.parch,
        "ticket": booking.ticket if booking else None,
        "fare": booking.fare if booking else None,
        "cabin": booking.cabin if booking else None,
        "embarked": booking.embarked if booking else None,
    }



class WalterRoasterPgRepository(WalterRoasterRepository):
    '''승객 명단 관리 저장소'''

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        logger.info("[WalterRoasterPgRepository] introduce_myself 진입 | request_data=%s", schema)
        return WalterRoasterResponse(
            id=schema.id * 10000,
            name=f"{schema.name}가 레포지토리에 다녀옴",
        )

    async def list_openfile_page(self, *, page: int, page_size: int) -> dict[str, Any]:
        logger.info(
            "[WalterRoasterPgRepository] list_openfile_page 진입 | page=%s page_size=%s",
            page,
            page_size,
        )
        safe_page_size = max(1, min(int(page_size), 200))
        safe_page = max(1, int(page))
        offset = (safe_page - 1) * safe_page_size

        count_result = await self.session.execute(
            select(func.count()).select_from(PersonOrm)
        )
        total = int(count_result.scalar_one())

        result = await self.session.execute(
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

        return {
            "page": safe_page,
            "pageSize": safe_page_size,
            "total": total,
            "items": items,
        }
