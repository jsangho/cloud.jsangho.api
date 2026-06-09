from __future__ import annotations

from core.matrix.grid_oracle_database_manager import LAYER_LOG
from kayfabe.app.dtos.records_dto import (
    CompetitorListDto,
    CompetitorMatchRecordDto,
    CompetitorProfileDto,
    CompetitorSummaryDto,
)
from kayfabe.app.ports.input.records_use_case import RecordsUseCase
from kayfabe.app.ports.output.records_repository import RecordsRepository
from kayfabe.app.services.records_scoring import (
    competitor_name_in_card_json,
    derive_match_record_from_orm,
    normalize_name,
)

logger = LAYER_LOG


class RecordsInteractor(RecordsUseCase):
    def __init__(
        self,
        *,
        records_repository: RecordsRepository,
    ) -> None:
        self._records = records_repository

    async def list_competitors(self, *, q: str | None = None) -> CompetitorListDto:
        logger.info("[RecordsInteractor] list_competitors -> Repository q=%s", q or "-")
        names = await self._records.list_competitor_names()
        if q:
            needle = q.strip().lower()
            names = [n for n in names if needle in n.lower()]
        logger.info("[RecordsInteractor] list_competitors <- Repository count=%d", len(names))
        return CompetitorListDto(names=names)

    async def get_competitor_profile(self, name: str) -> CompetitorProfileDto:
        normalized = normalize_name(name)
        logger.info("[RecordsInteractor] get_competitor_profile -> Repository name=%s", normalized)

        matches: list[CompetitorMatchRecordDto] = []
        snapshots = await self._records.list_match_snapshots()
        for event, match in snapshots:
            if not match.card_json:
                continue
            if not competitor_name_in_card_json(card_json=match.card_json, name=normalized):
                continue
            rec = derive_match_record_from_orm(
                event_slug=event.slug,
                event_label=event.label,
                match_key=match.match_key,
                title=match.title,
                format=match.format,
                card_json=match.card_json,
                winner_pick=match.winner_pick,
                winner_name=match.winner_name,
                status=match.status,
                name=normalized,
            )
            matches.append(
                CompetitorMatchRecordDto(
                    slug=rec.slug,
                    ple_label=rec.ple_label,
                    match_key=rec.match_key,
                    title=rec.title,
                    format=rec.format,
                    result=rec.result,
                    winner_name=rec.winner_name,
                    opponents=list(rec.opponents),
                    participants=list(rec.participants),
                    was_champion=rec.was_champion,
                )
            )

        singles_total = sum(1 for m in matches if m.format == "singles")
        multi_total = sum(1 for m in matches if m.format == "multi")
        champion_appearances = sum(1 for m in matches if m.was_champion)

        summary = CompetitorSummaryDto(
            total=len(matches),
            wins=sum(1 for m in matches if m.result == "win"),
            losses=sum(1 for m in matches if m.result == "loss"),
            no_contest=sum(1 for m in matches if m.result == "no-contest"),
            pending=sum(1 for m in matches if m.result == "pending"),
            singles_total=singles_total,
            multi_total=multi_total,
            champion_appearances=champion_appearances,
        )

        logger.info(
            "[RecordsInteractor] get_competitor_profile <- name=%s matches=%d",
            normalized,
            len(matches),
        )
        return CompetitorProfileDto(name=normalized, matches=matches, summary=summary)
