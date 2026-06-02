from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.james_director_dto import BookingCommand, PersonCommand


class JamesDirectorRepository(ABC):
    """James Director 업로드 데이터 영속화 출력 포트."""

    @abstractmethod
    async def save_fileupload_rows(
        self,
        *,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand]
        ,
        filename: str,
        rows: list[dict[str, object]],
    ) -> int:
        ...
