from __future__ import annotations

from pathlib import Path
from typing import Any

from core.database import james_director_upload_info
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.james_director_repository import JamesDirectorRepository

_SRC = Path(__file__).name


class JamesDirectorInteractor(JamesDirectorUseCase):
    """James Director CSV 업로드 유스케이스."""

    def __init__(self, repository: JamesDirectorRepository) -> None:
        self._repository = repository

    async def fileupload(
        self,
        *,
        filename: str,
        rows: list[dict[str, Any]],
    ) -> dict[str, int]:
        james_director_upload_info(_SRC, "file=%s -> use_case", filename)
        inserted = await self._repository.save_fileupload_rows(
            filename=filename, rows=rows
        )
        return {"count": inserted}
