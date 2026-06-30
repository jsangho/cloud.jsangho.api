from __future__ import annotations

from abc import ABC, abstractmethod

from manager.app.dtos.juso_dto import (
    ContactListItem,
    ContactRecordCommand,
    JusoQuery,
    JusoResponse,
)


class JusoUseCase(ABC):
    """`/manager/juso/*` inbound 입력 포트."""

    @abstractmethod
    async def introduce_myself(self, query: JusoQuery) -> JusoResponse:
        """주소 검색 서비스 자기소개."""
        ...

    @abstractmethod
    async def upload_contacts(
        self, commands: list[ContactRecordCommand]
    ) -> dict[str, int]:
        """Google Contacts CSV 업로드."""
        ...

    @abstractmethod
    async def list_contacts(self) -> list[ContactListItem]:
        """등록된 연락처 목록 조회."""
        ...
