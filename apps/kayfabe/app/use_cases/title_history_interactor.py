from __future__ import annotations

from kayfabe.app.dtos.title_history_dto import CompetitorTitleHistoryDto, TitleAcquisitionDto
from kayfabe.app.ports.input.title_history_use_case import TitleHistoryUseCase
from kayfabe.app.ports.output.title_history_repository import TitleHistoryRepository
from kayfabe.app.services.records_scoring import normalize_name


class TitleHistoryInteractor(TitleHistoryUseCase):
    def __init__(self, *, title_history_repository: TitleHistoryRepository) -> None:
        self._title_history = title_history_repository

    async def sync_from_real_catalog(self) -> int:
        return await self._title_history.sync_from_real_catalog()

    async def _ensure_catalog_loaded(self) -> None:
        if await self._title_history.needs_real_resync():
            await self.sync_from_real_catalog()

    async def get_competitor_title_history(self, name: str) -> CompetitorTitleHistoryDto:
        normalized = normalize_name(name)
        await self._ensure_catalog_loaded()
        rows = await self._title_history.list_by_competitor(competitor_name=normalized)
        return CompetitorTitleHistoryDto(
            name=normalized,
            acquisitions=[
                TitleAcquisitionDto(
                    belt_name=row.belt_name,
                    won_at=row.won_at,
                    won_at_slug=row.won_at_slug,
                    match_key=row.match_key,
                )
                for row in rows
            ],
        )
