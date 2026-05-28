from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LAYER_LOG
from titanic.adapter.outbound.pg.james_pg_repository import JamesPgRepository

logger = LAYER_LOG
_SRC = Path(__file__).name


class JamesRepositoryPort(Protocol):
    """James 업로드 데이터를 영속화하는 출력 포트."""

    async def save_fileupload_rows(
        self, *, filename: str, rows: list[dict[str, Any]]
    ) -> int: ...


@dataclass(slots=True)
class JamesRepositoryResult:
    inserted: int


class JamesRepositoryImpl:
    """출력 포트 구현 — PG 어댑터로 위임."""

    def __init__(self, db: AsyncSession) -> None:
        self._pg = JamesPgRepository(db)

    async def save_fileupload_rows(self, *, filename: str, rows: list[dict[str, Any]]) -> int:
        logger.info("[JamesUpload][%s] file=%s -> output_port(repository)", _SRC, filename)
        inserted = await self._pg.save_fileupload_rows(filename=filename, rows=rows)
        return JamesRepositoryResult(inserted=inserted).inserted
