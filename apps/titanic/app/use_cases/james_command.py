from __future__ import annotations

from pathlib import Path
from typing import Any

from core.database import james_upload_info
from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.ports.output.james_repository import JamesRepository

_SRC = Path(__file__).name


class JamesCommand(JamesUseCase):
    """James CSV 업로드: router 데이터 → repository 영속화."""

    async def fileupload(
        self,
        *,
        repository: JamesRepository,
        filename: str,
        rows: list[dict[str, Any]],
    ) -> dict[str, int]:
        james_upload_info(_SRC, "file=%s -> use_case", filename)
        inserted = await repository.save_fileupload_rows(filename=filename, rows=rows)
        return {"count": inserted}
