from __future__ import annotations

import logging

from core.matrix.grid_oracle_database_manager import AsyncSessionLocal, Base, engine
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.crew_james_director_schema import (
    JamesDirectorMyselfSchema,
    format_preview_booking_command,
    format_preview_person_command,
)
from titanic.adapter.outbound.orm.booking_orm import BookingOrm
from titanic.adapter.outbound.orm.person_orm import PersonOrm
from titanic.app.dtos.crew_james_director_dto import BookingCommand, JamesDirectorResponse, PersonCommand
from titanic.app.ports.output.crew_james_director_repository import JamesDirectorRepository

logger = logging.getLogger("uvicorn.error")

_BULK_CHUNK_SIZE = 300


def _parse_optional_int(raw: str) -> int | None:
    value = (raw or "").strip()
    if not value:
        return None
    return int(float(value))


def _parse_optional_float(raw: str) -> float | None:
    value = (raw or "").strip()
    if not value:
        return None
    return float(value)


def _parse_passenger_id(raw: str) -> int | None:
    value = (raw or "").strip()
    if not value:
        return None
    return int(float(value))


def _person_fields(cmd: PersonCommand, passenger_id: int) -> dict[str, object]:
    return {
        "passenger_id": passenger_id,
        "name": cmd.name.strip() or None,
        "gender": cmd.gender.strip() or None,
        "age": _parse_optional_float(cmd.age),
        "sib_sp": _parse_optional_int(cmd.sib_sp),
        "parch": _parse_optional_int(cmd.parch),
        "survived": _parse_optional_int(cmd.survived),
    }


def _booking_fields(cmd: BookingCommand) -> dict[str, object]:
    cabin = cmd.cabin.strip() or None
    embarked = cmd.embarked.strip() or None
    return {
        "pclass": _parse_optional_int(cmd.pclass),
        "ticket": (cmd.ticket.strip() or None)[:64] if cmd.ticket.strip() else None,
        "fare": _parse_optional_float(cmd.fare),
        "cabin": cabin[:32] if cabin else None,
        "embarked": embarked[:1] if embarked else None,
    }


async def _ensure_james_director_tables() -> None:
    """Neon에 persons / bookings 테이블이 없으면 생성."""
    if engine is None:
        raise HTTPException(
            status_code=503,
            detail="DATABASE_URL이 .env 등에 설정되지 않았습니다.",
        )
    import titanic.adapter.outbound.orm.booking_orm  # noqa: F401
    import titanic.adapter.outbound.orm.person_orm  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class JamesDirectorPgRepository(JamesDirectorRepository):
    """Neon(Postgres) James Director 업로드 어댑터."""

    def __init__(self, session: AsyncSession | None) -> None:
        self._session = session

    async def introduce_myself(self, schema: JamesDirectorMyselfSchema) -> JamesDirectorResponse:
        
        '''제임스 디렉터의 자기 소개 레포지토리 구현 메소드'''

        logger.info("[JamesDirectorPgRepository] introduce_myself 진입 | request_data=%s", schema)
        
        response: JamesDirectorResponse = JamesDirectorResponse(
            id= schema.id * 10000,
            name= schema.name + "가 레포지토리에 다녀옴"
        )
        return response

    async def upload_titanic_file(
        self,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
        filename: str,
    ) -> int:
        if AsyncSessionLocal is None:
            raise HTTPException(
                status_code=503,
                detail="DATABASE_URL이 .env 등에 설정되지 않았습니다.",
            )

        await _ensure_james_director_tables()

        if person_commands:
            limit = min(5, len(person_commands))
            logger.info(
                "[제임스 레포지토리] PersonCommand 인코딩 미리보기 (순위 %s번)",
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
                "[제임스 레포지토리] BookingCommand 인코딩 미리보기 (순위 %s번)",
                limit,
            )
            preview_blocks = [
                format_preview_booking_command(index, cmd)
                for index, cmd in enumerate(booking_commands[:5], start=1)
            ]
            if preview_blocks:
                logger.info("\n%s", "\n".join(preview_blocks))

        if self._session is None:
            async with AsyncSessionLocal() as session:
                saved = await self._save_person_and_booking_commands(
                    session=session,
                    person_commands=person_commands,
                    booking_commands=booking_commands,
                )
                await session.commit()
        else:
            saved = await self._save_person_and_booking_commands(
                session=self._session,
                person_commands=person_commands,
                booking_commands=booking_commands,
            )
            await self._session.commit()

        logger.info(
            "[제임스 레포지토리] upload done: file=%s persons/bookings=%s rows=%s",
            filename,
            saved,
            len(person_commands),
        )
        return len(person_commands)

    async def _save_person_and_booking_commands(
        self,
        *,
        session: AsyncSession,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
    ) -> int:
        pairs: list[tuple[int, dict[str, object], dict[str, object]]] = []
        for person_cmd, booking_cmd in zip(person_commands, booking_commands):
            passenger_id = _parse_passenger_id(person_cmd.passenger_id)
            if passenger_id is None:
                continue
            pairs.append(
                (
                    passenger_id,
                    _person_fields(person_cmd, passenger_id),
                    _booking_fields(booking_cmd),
                )
            )

        if not pairs:
            return 0

        person_values = [person_data for _, person_data, _ in pairs]
        for chunk_start in range(0, len(person_values), _BULK_CHUNK_SIZE):
            chunk = person_values[chunk_start : chunk_start + _BULK_CHUNK_SIZE]
            person_insert = pg_insert(PersonOrm).values(chunk)
            await session.execute(
                person_insert.on_conflict_do_update(
                    index_elements=[PersonOrm.passenger_id],
                    set_={
                        "name": person_insert.excluded.name,
                        "gender": person_insert.excluded.gender,
                        "age": person_insert.excluded.age,
                        "sib_sp": person_insert.excluded.sib_sp,
                        "parch": person_insert.excluded.parch,
                        "survived": person_insert.excluded.survived,
                    },
                )
            )

        passenger_ids = [passenger_id for passenger_id, _, _ in pairs]
        person_id_by_passenger: dict[int, int] = {}
        for chunk_start in range(0, len(passenger_ids), _BULK_CHUNK_SIZE):
            chunk_ids = passenger_ids[chunk_start : chunk_start + _BULK_CHUNK_SIZE]
            result = await session.execute(
                select(PersonOrm.passenger_id, PersonOrm.id).where(
                    PersonOrm.passenger_id.in_(chunk_ids)
                )
            )
            person_id_by_passenger.update(dict(result.all()))

        booking_values: list[dict[str, object]] = []
        for passenger_id, _, booking_data in pairs:
            person_id = person_id_by_passenger.get(passenger_id)
            if person_id is None:
                continue
            booking_values.append({"person_id": person_id, **booking_data})

        for chunk_start in range(0, len(booking_values), _BULK_CHUNK_SIZE):
            chunk = booking_values[chunk_start : chunk_start + _BULK_CHUNK_SIZE]
            booking_insert = pg_insert(BookingOrm).values(chunk)
            await session.execute(
                booking_insert.on_conflict_do_update(
                    constraint="uq_titanic_bookings_person_id",
                    set_={
                        "pclass": booking_insert.excluded.pclass,
                        "ticket": booking_insert.excluded.ticket,
                        "fare": booking_insert.excluded.fare,
                        "cabin": booking_insert.excluded.cabin,
                        "embarked": booking_insert.excluded.embarked,
                    },
                )
            )

        return len(pairs)
