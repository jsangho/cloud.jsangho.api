from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from manager.app.dtos.telegram_dto import TelegramQuery, TelegramResponse
from manager.app.ports.output.telegram_repository import TelegramRepository


class TelegramPgRepository(TelegramRepository):
    """Neon(Postgres) Telegram 메시지 로그 어댑터."""

    def __init__(self, session: AsyncSession | None = None) -> None:
        self._session = session

    async def introduce_myself(self, query: TelegramQuery) -> TelegramResponse:
        return TelegramResponse(
            id=query.id,
            name=query.name,
            description="Telegram 채널에 알림·보고서를 전송하는 봇 서비스입니다.",
        )
