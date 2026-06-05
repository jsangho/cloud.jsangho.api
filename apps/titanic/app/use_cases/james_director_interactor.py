from __future__ import annotations

import logging
from typing import Any

from titanic.adapter.inbound.api.schemas.james_director_schema import (
    TitanicRecordSchema,
    format_preview_record,
)
from titanic.app.dtos.james_director_dto import BookingCommand, PersonCommand
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.james_director_repository import JamesDirectorRepository

logger = logging.getLogger("uvicorn.error")

class JamesDirectorInteractor(JamesDirectorUseCase):
    """James Director CSV 업로드 유스케이스."""

    def __init__(self, repository: JamesDirectorRepository) -> None:
        self._repository = repository

    async def upload_titanic_file(
        self, records: list[TitanicRecordSchema]
    ) -> dict[str, int]:
        return await self.receive_uploaded_records(records)

    async def receive_uploaded_records(
        self,
        schema: list[TitanicRecordSchema],
        *,
        filename: str = "",
    ) -> dict[str, Any]:
        logger.info(
            "[제임스 유스케이스] 라우터에서 유스케이스로 옮겨진 스키마 레코드 미리보기 (상위 %s건)",
            min(5, len(schema)),
        )
        preview_blocks = [
            format_preview_record(index, record)
            for index, record in enumerate(schema[:5], start=1)
        ]
        if preview_blocks:
            logger.info("\n%s", "\n".join(preview_blocks))

        # schema 를 PersonCommand, BookingCommand 로 나눠서 옮겨담기

        person_commands: list[PersonCommand] = []
        booking_commands: list[BookingCommand] = []

        for record in schema:
            person_commands.append(
                PersonCommand(
                    passenger_id=record.passenger_id or "",
                    name=record.name or "",
                    gender=record.gender or "",
                    age=record.age or "",
                    sib_sp=record.sib_sp or "",
                    parch=record.parch or "",
                    survived=record.survived or "",
                )
            )
            booking_commands.append(
                BookingCommand(
                    pclass=record.pclass or "",
                    ticket=record.ticket or "",
                    fare=record.fare or "",
                    cabin=record.cabin or "",
                    embarked=record.embarked or "",
                )
            )

        count = await self._repository.upload_titanic_file(
            person_commands=person_commands,
            booking_commands=booking_commands,
            filename=filename,
        )
        return {"count": count}
