from __future__ import annotations

from core.matrix.grid_oracle_database_manager import AsyncSessionLocal
from sqlalchemy import select, update

from manager.adapter.outbound.orm.received_orm import ReceivedOrm
from manager.app.dtos.received_dto import ReceivedCommand, ReceivedItem
from manager.app.ports.output.received_repository import ReceivedRepository


class ReceivedPgRepository(ReceivedRepository):
    async def save(self, cmd: ReceivedCommand) -> int:
        async with AsyncSessionLocal() as session:
            orm = ReceivedOrm(
                from_email=cmd.from_email,
                from_name=cmd.from_name or None,
                to_email=cmd.to_email or None,
                subject=cmd.subject or None,
                body=cmd.body or None,
                message_id=cmd.message_id or None,
            )
            session.add(orm)
            await session.commit()
            await session.refresh(orm)
            return orm.id

    async def list_all(self) -> list[ReceivedItem]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ReceivedOrm).order_by(ReceivedOrm.received_at.desc())
            )
            rows = result.scalars().all()
        return [
            ReceivedItem(
                id=r.id,
                from_email=r.from_email,
                from_name=r.from_name or "",
                to_email=r.to_email or "",
                subject=r.subject or "",
                body=r.body or "",
                message_id=r.message_id or "",
                received_at=r.received_at,
                is_read=r.is_read,
            )
            for r in rows
        ]

    async def mark_read(self, item_id: int) -> None:
        async with AsyncSessionLocal() as session:
            await session.execute(
                update(ReceivedOrm)
                .where(ReceivedOrm.id == item_id)
                .values(is_read=True)
            )
            await session.commit()
