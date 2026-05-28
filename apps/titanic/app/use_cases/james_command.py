from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core.database import LAYER_LOG
from titanic.app.ports.output.james_repository import JamesRepositoryPort

logger = LAYER_LOG
_SRC = Path(__file__).name


@dataclass(slots=True)
class JamesCommandResult:
    count: int


class JamesCommand:
    """James CSV 업로드 커맨드 유스케이스."""

    def __init__(self, repository: JamesRepositoryPort) -> None:
        self._repository = repository

    async def handle_fileupload(
        self, *, filename: str, rows: list[dict[str, Any]]
    ) -> JamesCommandResult:
        logger.info("[JamesUpload][%s] file=%s -> command", _SRC, filename)
        inserted = await self._repository.save_fileupload_rows(filename=filename, rows=rows)
        return JamesCommandResult(count=inserted)
