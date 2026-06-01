from __future__ import annotations

from typing import Any

from titanic.app.ports.input.andrews_blueprint_use_case import AndrewsBlueprintUseCase
from titanic.app.ports.output.andrews_blueprint_repository import AndrewsBlueprintRepository


class AndrewsBlueprintInteractor(AndrewsBlueprintUseCase):
    """Andrews Blueprint 조회 유스케이스."""

    def __init__(self, repository: AndrewsBlueprintRepository) -> None:
        self._repository = repository

    async def get_blueprint(self) -> dict[str, Any]:
        return await self._repository.get_blueprint()
