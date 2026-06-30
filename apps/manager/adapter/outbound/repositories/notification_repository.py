from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import AsyncSessionLocal, Base, engine
from manager.adapter.outbound.orm.notification_orm import NotificationOrm
from manager.app.dtos.notification_dto import NotificationDto
from manager.app.ports.output.notification_repository import NotificationRepository


async def _ensure_notifications_table() -> None:
    """Neon에 notifications 테이블이 없으면 생성."""
    if engine is None:
        raise HTTPException(
            status_code=503,
            detail="DATABASE_URL이 .env 등에 설정되지 않았습니다.",
        )
    import manager.adapter.outbound.orm.notification_orm  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_notifications_to_email "
                "ON notifications (to_email)"
            )
        )


class NotificationPgRepository(NotificationRepository):
    """Neon(Postgres) 알림 발송 이력 어댑터."""

    def __init__(self, session: AsyncSession | None = None) -> None:
        self._session = session

    async def save(self, dto: NotificationDto, status: str) -> int:
        if AsyncSessionLocal is None:
            raise HTTPException(
                status_code=503,
                detail="DATABASE_URL이 .env 등에 설정되지 않았습니다.",
            )

        await _ensure_notifications_table()

        row = NotificationOrm(
            to_email=dto.to,
            subject=dto.subject,
            body=dto.body,
            status=status,
        )

        if self._session is None:
            async with AsyncSessionLocal() as session:
                session.add(row)
                await session.commit()
                await session.refresh(row)
        else:
            self._session.add(row)
            await self._session.commit()
            await self._session.refresh(row)

        return row.id
