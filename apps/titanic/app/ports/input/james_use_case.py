from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LAYER_LOG
from titanic.app.ports.output.james_repository import JamesRepositoryImpl, JamesRepositoryPort
from titanic.app.use_cases.james_command import JamesCommand

logger = LAYER_LOG
_SRC = Path(__file__).name


class JamesUseCasePort(Protocol):
    """`/titanic/james/*` inbound가 호출하는 입력 포트."""

    async def fileupload(
        self, *, filename: str, rows: list[dict[str, Any]]
    ) -> dict[str, Any]: ...


@dataclass(slots=True)
class JamesFileUploadResult:
    count: int


class JamesUseCaseImpl:
    def __init__(
        self,
        repository: JamesRepositoryPort | None = None,
        *,
        db: AsyncSession | None = None,
    ) -> None:
        if repository is None:
            if db is None:
                raise ValueError("JamesUseCaseImpl requires db or repository")
            repository = JamesRepositoryImpl(db)
        self._repository = repository

    async def fileupload(self, *, filename: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
        logger.info("[JamesUpload][%s] file=%s -> use_case", _SRC, filename)
        result = await JamesCommand(self._repository).handle_fileupload(filename=filename, rows=rows)
        return {"count": JamesFileUploadResult(count=result.count).count}
