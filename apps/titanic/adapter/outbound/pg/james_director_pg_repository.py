from __future__ import annotations

import logging

from core.database import AsyncSessionLocal
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.james_director_schema import (
    format_preview_booking_command,
    format_preview_person_command,
)
from titanic.app.ports.output.james_director_repository import JamesDirectorRepository
from titanic.app.dtos.james_director_dto import BookingCommand, PersonCommand
from titanic.domain.entities.passenger_model import PassengerModel

logger = logging.getLogger("uvicorn.error")


class JamesDirectorPgRepository(JamesDirectorRepository):
    """Neon(Postgres) `titanic_passengers` 업로드 어댑터."""
    def __init__(self, session: AsyncSession | None) -> None:
        self._session = session

    async def save_fileupload_rows(
        self,
        *,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
        filename: str,
        rows: list[dict[str, object]],
    ) -> int:
        if AsyncSessionLocal is None:
            raise HTTPException(
                status_code=503,
                detail="DATABASE_URL이 .env 등에 설정되지 않았습니다.",
            )

        if person_commands:
            limit = min(5, len(person_commands))
            logger.info(
                "[제임스 레포지토리] PersonCommand 레코드 미리보기 (상위 %s건)",
                limit,
            )
            preview_blocks = [
                format_preview_person_command(index, cmd)
                for index, cmd in enumerate(person_commands[:5], start=1)
            ]
            if preview_blocks:
                logger.info("\n%s", "\n".join(preview_blocks))
        if booking_commands:
            limit = min(5, len(booking_commands))
            logger.info(
                "[제임스 레포지토리] BookingCommand 레코드 미리보기 (상위 %s건)",
                limit,
            )
            preview_blocks = [
                format_preview_booking_command(index, cmd)
                for index, cmd in enumerate(booking_commands[:5], start=1)
            ]
            if preview_blocks:
                logger.info("\n%s", "\n".join(preview_blocks))

        saved = 0
        if self._session is None:
            async with AsyncSessionLocal() as session:
                saved = await self._upsert_rows(session=session, rows=rows)
                await session.commit()
        else:
            saved = await self._upsert_rows(session=self._session, rows=rows)
            await self._session.commit()

        logger.info(
            "[제임스 레포지토리] upload done: file=%s saved=%s rows=%s",
            filename,
            saved,
            len(rows),
        )
        return len(rows)

    async def _upsert_rows(
        self, *, session: AsyncSession, rows: list[dict[str, object]]
    ) -> int:
        saved = 0
        for row in rows:
            passenger_id_raw = row.get("PassengerId")
            if passenger_id_raw is None:
                continue
            passenger_id = int(float(str(passenger_id_raw)))

            result = await session.execute(
                select(PassengerModel).where(PassengerModel.passenger_id == passenger_id)
            )
            entity = result.scalar_one_or_none()

            fields = {
                "passenger_id": passenger_id,
                "survived": int(float(row["Survived"])) if row.get("Survived") not in (None, "") else None,
                "pclass": int(float(row["Pclass"])) if row.get("Pclass") not in (None, "") else None,
                "name": row.get("Name") or None,
                "sex": (row.get("gender") or row.get("Sex")) or None,
                "age": float(row["Age"]) if row.get("Age") not in (None, "") else None,
                "sibsp": int(float(row["SibSp"])) if row.get("SibSp") not in (None, "") else None,
                "parch": int(float(row["Parch"])) if row.get("Parch") not in (None, "") else None,
                "ticket": row.get("Ticket") or None,
                "fare": float(row["Fare"]) if row.get("Fare") not in (None, "") else None,
                "cabin": row.get("Cabin") or None,
                "embarked": row.get("Embarked") or None,
            }

            if entity is None:
                session.add(PassengerModel(**fields))
                saved += 1
            else:
                for key, value in fields.items():
                    setattr(entity, key, value)

        return saved
