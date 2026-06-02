from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.james_director_schema import TitanicRecordSchema


class JamesDirectorUseCase(ABC):
    """`/titanic/james-director/*` inbound(james_director_router) 입력 포트."""

    @abstractmethod
    async def save_fileupload_rows(self, records: list[TitanicRecordSchema]) -> dict[str, int]:
        """CSV 업로드 (`POST /fileupload`)."""
        ...


def get_james_director_use_case() -> JamesDirectorUseCase:
    """
    Composition root(예: `backend/main.py`)에서 override 되는 유스케이스 의존성입니다.

    라우터는 레포지토리 구현체를 알지 않고, 이 함수에만 의존합니다.
    """
    raise RuntimeError(
        "get_james_director_use_case dependency is not configured. "
        "Set FastAPI dependency_overrides in the composition root."
    )
