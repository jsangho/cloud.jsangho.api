from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.james_director_schema import TitanicRecordSchema


class JamesDirectorUseCase(ABC):
    """`/titanic/james-director/*` inbound(james_director_router) 입력 포트."""

    @abstractmethod
    async def upload_titanic_file(self, records: list[TitanicRecordSchema]) -> dict[str, int]:
        """CSV 업로드 (`POST /fileupload`)."""
        ...
