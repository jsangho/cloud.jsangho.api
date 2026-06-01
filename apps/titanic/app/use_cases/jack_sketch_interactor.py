from __future__ import annotations

from typing import Any

from titanic.app.ports.input.jack_sketch_use_case import JackSketchUseCase
from titanic.app.ports.output.jack_sketch_repository import JackSketchRepository


class JackSketchInteractor(JackSketchUseCase):
    """Jack 스케치 조회 유스케이스."""

    def __init__(self, repository: JackSketchRepository) -> None:
        self._repository = repository

    async def get_sketch(self) -> dict[str, Any]:
        return await self._repository.get_sketch()
