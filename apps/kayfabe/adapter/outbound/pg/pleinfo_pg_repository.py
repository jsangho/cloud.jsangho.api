import json

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.matrix.grid_oracle_database_manager import LAYER_LOG
from kayfabe.adapter.outbound.mappers.ple_orm_mapper import event_to_read
from kayfabe.adapter.outbound.orm.ple_orm import PleEventModel, PleMatchModel, PlePredictionModel
from kayfabe.app.dtos.ple_dto import PleAiRecordDto, PleAiStatsDto, PleEventReadDto
from kayfabe.app.ports.output.pleinfo_repository import PleInfoRepository

logger = LAYER_LOG


class PleInfoPgRepository(PleInfoRepository):
    """Neon(Postgres) PLE 조회 어댑터."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def _load_event_model(self, slug: str, *, with_predictions: bool) -> PleEventModel | None:
        stmt = select(PleEventModel).where(PleEventModel.slug == slug)
        if with_predictions:
            stmt = stmt.options(
                selectinload(PleEventModel.matches).selectinload(PleMatchModel.predictions)
            )
        else:
            stmt = stmt.options(selectinload(PleEventModel.matches))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_events(self) -> list[PleEventReadDto]:
        logger.info("[PleInfoPgRepository] list_events -> Neon")
        result = await self.db.execute(
            select(PleEventModel)
            .options(selectinload(PleEventModel.matches))
            .order_by(PleEventModel.month)
        )
        rows = [event_to_read(e) for e in result.scalars().all()]
        logger.info("[PleInfoPgRepository] list_events <- Neon | count=%d", len(rows))
        return rows

    async def get_event_by_slug(self, slug: str) -> PleEventReadDto | None:
        logger.info("[PleInfoPgRepository] get_event_by_slug -> Neon | slug=%s", slug)
        event = await self._load_event_model(slug, with_predictions=True)
        if event is None:
            return None
        return event_to_read(event)

    async def get_prediction_pick_by_user(self, match_id: int, user_id: int) -> str | None:
        result = await self.db.execute(
            select(PlePredictionModel.pick).where(
                PlePredictionModel.match_id == match_id,
                PlePredictionModel.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_prediction_pick(self, match_id: int, client_id: str) -> str | None:
        result = await self.db.execute(
            select(PlePredictionModel.pick).where(
                PlePredictionModel.match_id == match_id,
                PlePredictionModel.client_id == client_id,
            )
        )
        return result.scalar_one_or_none()

    async def aggregate_votes_for_match(
        self, *, match_id: int, fmt: str, card_json: str
    ) -> dict[str, int | list[int]]:
        result = await self.db.execute(
            select(PlePredictionModel.pick).where(PlePredictionModel.match_id == match_id)
        )
        picks = list(result.scalars().all())

        if fmt == "multi":
            card = json.loads(card_json)
            count = len(card.get("competitors") or [])
            totals: list[int] = [0] * count
            for pick in picks:
                try:
                    idx = int(pick)
                    if 0 <= idx < count:
                        totals[idx] += 1
                except ValueError:
                    continue
            return {"left": 0, "right": 0, "multi": totals}

        left = sum(1 for p in picks if p == "left")
        right = sum(1 for p in picks if p == "right")
        return {"left": left, "right": right, "multi": []}

    async def get_ai_stats(self) -> PleAiStatsDto:
        logger.info("[PleInfoPgRepository] get_ai_stats -> Neon")
        agg = await self.db.execute(
            select(
                func.count(PleMatchModel.id),
                func.coalesce(
                    func.sum(case((PleMatchModel.ai_correct.is_(True), 1), else_=0)), 0
                ),
            ).where(PleMatchModel.ai_correct.isnot(None))
        )
        total_graded, correct = agg.one()
        total_graded = int(total_graded or 0)
        correct = int(correct or 0)
        incorrect = max(0, total_graded - correct)
        accuracy = round(correct / total_graded * 100, 1) if total_graded > 0 else None

        recent_rows = await self.db.execute(
            select(PleMatchModel, PleEventModel)
            .join(PleEventModel, PleMatchModel.event_id == PleEventModel.id)
            .where(PleMatchModel.ai_correct.isnot(None))
            .order_by(
                PleEventModel.year.asc(),
                PleEventModel.month.asc().nulls_last(),
                PleEventModel.slug.asc(),
                PleMatchModel.sort_order.asc(),
                PleMatchModel.id.asc(),
            )
        )
        recent = [
            PleAiRecordDto(
                event_slug=event.slug,
                event_label=event.label,
                match_key=match.match_key,
                match_title=match.title,
                ai_pick_name=match.ai_pick_name or "",
                winner_name=match.winner_name,
                correct=bool(match.ai_correct),
            )
            for match, event in recent_rows.all()
        ]

        stats = PleAiStatsDto(
            total_graded=total_graded,
            correct=correct,
            incorrect=incorrect,
            accuracy_percent=accuracy,
            recent=recent,
        )
        logger.info("[PleInfoPgRepository] get_ai_stats <- Neon | graded=%d", total_graded)
        return stats
