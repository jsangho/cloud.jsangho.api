from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_james_director_dto import BookingCommand, PersonCommand
from titanic.adapter.inbound.api.schemas.crew_james_director_schema import JamesDirectorMyselfSchema
from titanic.app.dtos.crew_james_director_dto import JamesDirectorResponse


class JamesDirectorRepository(ABC):
    """CSV 업로드 데이터 영속화 출력 포트."""

    @abstractmethod
    async def introduce_myself(self, schema: JamesDirectorMyselfSchema) -> JamesDirectorResponse:
        '''제임스 디렉터의 자기소개 메소드'''
        pass

    @abstractmethod
    async def upload_titanic_file(
        self,
        *,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
        filename: str,
    ) -> int:
        ...
