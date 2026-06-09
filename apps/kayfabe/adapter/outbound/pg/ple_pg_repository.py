import json
from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import LAYER_LOG
from friday13th.domain.entities.user_model import UserModel
from kayfabe.adapter.outbound.mappers.ple_orm_mapper import card_command_to_json, event_to_snapshot
from kayfabe.adapter.outbound.pg.pleinfo_pg_repository import PleInfoPgRepository
from kayfabe.app.dtos.ple_dto import MatchResultDto, PleEventSnapshotDto, PleEventSyncCommand
from kayfabe.app.ports.output.ple_repository import PleRepository
from kayfabe.adapter.outbound.orm.ple_orm import (
    PleEventModel,
    PleEventStatus,
    PleMatchModel,
    PleMatchStatus,
    PlePredictionModel,
)
from kayfabe.app.services.ple_ai import derive_ai_pick_from_card, grade_ai_correct
from kayfabe.app.services.ple_scoring import (
    competitor_count_from_card,
    derive_match_point_value,
)

logger = LAYER_LOG


class PlePgRepository(PleRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self._info = PleInfoPgRepository(db)

    async def user_exists(self, *, user_id: int) -> bool:
        result = await self.db.execute(select(UserModel.id).where(UserModel.id == user_id))
        return result.scalar_one_or_none() is not None

    async def flush(self) -> None:
        await self.db.flush()

    async def _get_event_orm(self, slug: str) -> PleEventModel | None:
        return await self._info._load_event_model(slug, with_predictions=False)

    async def get_event_by_slug(self, slug: str) -> PleEventSnapshotDto | None:
        event = await self._get_event_orm(slug)
        if event is None:
            return None
        return event_to_snapshot(event)

    async def upsert_event_from_sync(self, payload: PleEventSyncCommand) -> PleEventSnapshotDto:
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

        event = await self._get_event_orm(payload.slug)
        if event is None:
            raise RuntimeError(f"PLE event upsert failed: slug={payload.slug!r}")

        if payload.status:
            event.status = payload.status

        existing = {m.match_key: m for m in event.matches}
        seen_keys: set[str] = set()

        for order, card in enumerate(payload.matches):
            seen_keys.add(card.id)
            card_json = card_command_to_json(card)
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
        refreshed = await self._get_event_orm(payload.slug)
        if refreshed is None:
            raise RuntimeError(f"PLE event upsert failed: slug={payload.slug!r}")
        return event_to_snapshot(refreshed)

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

    def _apply_result_to_row(self, row: PleMatchModel, result: MatchResultDto) -> None:
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
        result: MatchResultDto,
        status: str | None = None,
    ) -> bool:
        event = await self._get_event_orm(slug)
        if event is None:
            return False
        row = next((m for m in event.matches if m.match_key == match_key), None)
        if row is None:
            return False
        self._apply_result_to_row(row, result)
        if status:
            row.status = status
        await self.db.flush()
        return True

    async def mark_event_finished(self, *, event_id: int, finished_at) -> None:
        result = await self.db.execute(
            select(PleEventModel)
            .where(PleEventModel.id == event_id)
            .options(selectinload(PleEventModel.matches))
        )
        event = result.scalar_one_or_none()
        if event is None:
            return
        event.status = PleEventStatus.FINISHED
        event.finished_at = finished_at
        for match in event.matches:
            if match.status != PleMatchStatus.FINISHED and match.winner_pick:
                match.status = PleMatchStatus.FINISHED
                match.finished_at = finished_at
        await self.db.flush()

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
            "[PleRepository] attach_user_id_by_client ??clientId=%s userId=%s linked=%s",
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
    ) -> None:
        existing = await self.get_prediction_by_user(match_id, user_id)
        if existing is not None:
            existing.pick = pick
            existing.client_id = client_id
            await self.db.flush()
            return
        await self.add_prediction(match_id, client_id, pick, user_id)

    async def add_prediction(
        self,
        match_id: int,
        client_id: str,
        pick: str,
        user_id: int | None = None,
    ) -> PlePredictionModel:
        logger.info(
            "[PleRepository] add_prediction -> Neon ??matchId=%s clientId=%s pick=%s",
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
            "[PleRepository] add_prediction <- Neon ??predictionId=%s",
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

