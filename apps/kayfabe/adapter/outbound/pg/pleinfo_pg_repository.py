import json

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.matrix.oracle_database import LAYER_LOG
from kayfabe.adapter.inbound.api.schemas.ple_schema import PleAiRecordSchema, PleAiStatsSchema
from kayfabe.app.ports.output.pleinfo_repository import PleInfoRepository
from kayfabe.adapter.outbound.orm.ple_orm import PleEventModel, PleMatchModel, PlePredictionModel

logger = LAYER_LOG


class PleInfoPgRepository(PleInfoRepository):
    """Neon(Postgres) PLE ì¡°í ?´ë??"""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_events(self) -> list[PleEventModel]:
        logger.info("[PleInfoPgRepository] list_events -> Neon")
        result = await self.db.execute(
            select(PleEventModel)
            .options(selectinload(PleEventModel.matches))
            .order_by(PleEventModel.month)
        )
        rows = list(result.scalars().all())
        logger.info("[PleInfoPgRepository] list_events <- Neon ??count=%d", len(rows))
        return rows

    async def get_event_by_slug(self, slug: str) -> PleEventModel | None:
        logger.info("[PleInfoPgRepository] get_event_by_slug -> Neon ??slug=%s", slug)
        result = await self.db.execute(
            select(PleEventModel)
            .where(PleEventModel.slug == slug)
            .options(
                selectinload(PleEventModel.matches).selectinload(PleMatchModel.predictions)
            )
        )
        return result.scalar_one_or_none()

    async def get_prediction_by_user(
        self, match_id: int, user_id: int
    ) -> PlePredictionModel | None:
        result = await self.db.execute(
            select(PlePredictionModel).where(
                PlePredictionModel.match_id == match_id,
                PlePredictionModel.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_prediction(
        self, match_id: int, client_id: str
    ) -> PlePredictionModel | None:
        result = await self.db.execute(
            select(PlePredictionModel).where(
                PlePredictionModel.match_id == match_id,
                PlePredictionModel.client_id == client_id,
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    def aggregate_votes(
        match: PleMatchModel,
    ) -> tuple[dict[str, int | list[int]], str | None]:
        if match.format == "multi":
            card = json.loads(match.card_json)
            count = len(card.get("competitors") or [])
            totals: list[int] = [0] * count
            for pred in match.predictions:
                try:
                    idx = int(pred.pick)
                    if 0 <= idx < count:
                        totals[idx] += 1
                except ValueError:
                    continue
            return {"left": 0, "right": 0, "multi": totals}, None

        left = sum(1 for p in match.predictions if p.pick == "left")
        right = sum(1 for p in match.predictions if p.pick == "right")
        return {"left": left, "right": right, "multi": []}, None

    async def get_ai_stats(self) -> PleAiStatsSchema:
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
        accuracy = (
            round(correct / total_graded * 100, 1) if total_graded > 0 else None
        )

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
            PleAiRecordSchema(
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

        stats = PleAiStatsSchema(
            total_graded=total_graded,
            correct=correct,
            incorrect=incorrect,
            accuracy_percent=accuracy,
            recent=recent,
        )
        logger.info("[PleInfoPgRepository] get_ai_stats <- Neon ??graded=%d", total_graded)
        return stats
