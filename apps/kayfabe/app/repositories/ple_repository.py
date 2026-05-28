import json
from collections import defaultdict
from datetime import datetime, timezone

from sqlalchemy import case, func, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.database import LAYER_LOG
from kayfabe.app.models.ple_model import (
    PleEventModel,
    PleEventStatus,
    PleMatchModel,
    PleMatchStatus,
    PlePredictionModel,
)
from kayfabe.app.schemas.ple_schema import (
    MatchCardSyncSchema,
    MatchResultSchema,
    PleAiRecordSchema,
    PleAiStatsSchema,
    PleEventSyncSchema,
)
from kayfabe.app.ple_ai import derive_ai_pick_from_card, grade_ai_correct
from kayfabe.app.ple_scoring import (
    competitor_count_from_card,
    derive_match_point_value,
)

logger = LAYER_LOG


class PleRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_event_by_slug(self, slug: str) -> PleEventModel | None:
        result = await self.db.execute(
            select(PleEventModel)
            .where(PleEventModel.slug == slug)
            .options(selectinload(PleEventModel.matches).selectinload(PleMatchModel.predictions))
        )
        return result.scalar_one_or_none()

    async def list_events(self) -> list[PleEventModel]:
        result = await self.db.execute(
            select(PleEventModel)
            .options(selectinload(PleEventModel.matches))
            .order_by(PleEventModel.month)
        )
        return list(result.scalars().all())

    async def upsert_event_from_sync(self, payload: PleEventSyncSchema) -> PleEventModel:
        status_val = payload.status or PleEventStatus.UPCOMING
        await self.db.execute(
            pg_insert(PleEventModel)
            .values(
                slug=payload.slug,
                label=payload.label,
                month=payload.month,
                year=payload.year,
                status=status_val,
            )
            .on_conflict_do_update(
                index_elements=["slug"],
                set_={
                    "label": payload.label,
                    "month": payload.month,
                    "year": payload.year,
                },
            )
        )
        await self.db.flush()

        event = await self.get_event_by_slug(payload.slug)
        if event is None:
            raise RuntimeError(f"PLE event upsert failed: slug={payload.slug!r}")

        if payload.status:
            event.status = payload.status

        existing = {m.match_key: m for m in event.matches}
        seen_keys: set[str] = set()

        for order, card in enumerate(payload.matches):
            seen_keys.add(card.id)
            card_json = card.model_dump(by_alias=True, mode="json")
            row = existing.get(card.id)
            if row is None:
                row = PleMatchModel(
                    event_id=event.id,
                    match_key=card.id,
                    title=card.title,
                    format=card.format,
                    card_variant=card.card_variant,
                    sort_order=order,
                    card_json=json.dumps(card_json, ensure_ascii=False),
                )
                self.db.add(row)
            else:
                row.title = card.title
                row.format = card.format
                row.card_variant = card.card_variant
                row.sort_order = order
                row.card_json = json.dumps(card_json, ensure_ascii=False)

            card_dict = json.loads(row.card_json)
            self._apply_point_value(row, card_dict)
            derived = derive_ai_pick_from_card(card_dict)
            if derived:
                row.ai_pick, row.ai_pick_name = derived

            if card.result:
                self._apply_result_to_row(row, card.result)
            self._grade_ai_row(row)

        for key, row in existing.items():
            if key not in seen_keys:
                await self.db.delete(row)

        await self.db.flush()
        return event

    @staticmethod
    def _apply_point_value(row: PleMatchModel, card_dict: dict) -> None:
        count = competitor_count_from_card(card_dict, row.format)
        row.point_value = derive_match_point_value(
            row.title,
            row.format,
            match_key=row.match_key,
            competitor_count=count,
        )

    async def refresh_all_match_point_values(self) -> int:
        result = await self.db.execute(select(PleMatchModel))
        updated = 0
        for row in result.scalars().all():
            card_dict = json.loads(row.card_json)
            prev = row.point_value
            self._apply_point_value(row, card_dict)
            if row.point_value != prev:
                updated += 1
        await self.db.flush()
        return updated

    def _apply_result_to_row(self, row: PleMatchModel, result: MatchResultSchema) -> None:
        if result.winner_side:
            row.winner_pick = result.winner_side
        elif result.winner_index is not None:
            row.winner_pick = str(result.winner_index)
        if result.winner_name:
            row.winner_name = result.winner_name
        if result.winner_side or result.winner_index is not None or result.winner_name:
            row.status = PleMatchStatus.FINISHED
            row.finished_at = datetime.now(timezone.utc)
        self._grade_ai_row(row)

    @staticmethod
    def _grade_ai_row(row: PleMatchModel) -> None:
        row.ai_correct = grade_ai_correct(row.ai_pick, row.winner_pick)

    async def set_match_result(
        self,
        slug: str,
        match_key: str,
        result: MatchResultSchema,
        status: str | None = None,
    ) -> PleMatchModel | None:
        event = await self.get_event_by_slug(slug)
        if event is None:
            return None
        row = next((m for m in event.matches if m.match_key == match_key), None)
        if row is None:
            return None
        self._apply_result_to_row(row, result)
        if status:
            row.status = status
        await self.db.flush()
        return row

    async def finalize_event(self, slug: str) -> PleEventModel | None:
        event = await self.get_event_by_slug(slug)
        if event is None:
            return None
        now = datetime.now(timezone.utc)
        event.status = PleEventStatus.FINISHED
        event.finished_at = now
        for match in event.matches:
            if match.status != PleMatchStatus.FINISHED and match.winner_pick:
                match.status = PleMatchStatus.FINISHED
                match.finished_at = now
        await self.db.flush()
        return event

    async def attach_user_id_by_client(self, client_id: str, user_id: int) -> int:
        result = await self.db.execute(
            update(PlePredictionModel)
            .where(
                PlePredictionModel.client_id == client_id,
                PlePredictionModel.user_id.is_(None),
            )
            .values(user_id=user_id)
        )
        await self.db.flush()
        count = result.rowcount if result.rowcount is not None else 0
        logger.info(
            "[PleRepository] attach_user_id_by_client — clientId=%s userId=%s linked=%s",
            client_id,
            user_id,
            count,
        )
        return count

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

    async def upsert_prediction(
        self,
        match_id: int,
        client_id: str,
        pick: str,
        user_id: int,
    ) -> PlePredictionModel:
        existing = await self.get_prediction_by_user(match_id, user_id)
        if existing is not None:
            existing.pick = pick
            existing.client_id = client_id
            await self.db.flush()
            return existing
        return await self.add_prediction(match_id, client_id, pick, user_id)

    async def add_prediction(
        self,
        match_id: int,
        client_id: str,
        pick: str,
        user_id: int | None = None,
    ) -> PlePredictionModel:
        logger.info(
            "[PleRepository] add_prediction -> Neon — matchId=%s clientId=%s pick=%s",
            match_id,
            client_id,
            pick,
        )
        prediction = PlePredictionModel(
            match_id=match_id,
            client_id=client_id,
            user_id=user_id,
            pick=pick,
        )
        self.db.add(prediction)
        await self.db.flush()
        logger.info(
            "[PleRepository] add_prediction <- Neon — predictionId=%s",
            prediction.id,
        )
        return prediction

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

        # PLE·카드 순서대로 전체 채점 기록 (최근 N건 제한 없음)
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

        return PleAiStatsSchema(
            total_graded=total_graded,
            correct=correct,
            incorrect=incorrect,
            accuracy_percent=accuracy,
            recent=recent,
        )
