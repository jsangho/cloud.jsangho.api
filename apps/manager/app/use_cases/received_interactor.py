from __future__ import annotations

import json as _json
import os

import httpx

from manager.app.dtos.received_dto import ReceivedCommand, ReceivedItem
from manager.app.ports.input.received_use_case import ReceivedUseCase
from manager.app.ports.output.received_repository import ReceivedRepository

_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")


async def _telegram_notify(subject: str, from_email: str) -> None:
    if not _BOT_TOKEN or not _CHAT_ID:
        return
    msg = f"📬 새 메일 도착\n발신자: {from_email}\n제목: {subject}"
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{_BOT_TOKEN}/sendMessage",
            content=_json.dumps(
                {"chat_id": _CHAT_ID, "text": msg}, ensure_ascii=False
            ).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=10.0,
        )


class ReceivedInteractor(ReceivedUseCase):
    def __init__(self, repository: ReceivedRepository) -> None:
        self._repository = repository

    async def receive(self, cmd: ReceivedCommand) -> dict[str, int]:
        item_id = await self._repository.save(cmd)
        await _telegram_notify(subject=cmd.subject, from_email=cmd.from_email)
        return {"id": item_id}

    async def list_inbox(self) -> list[ReceivedItem]:
        return await self._repository.list_all()

    async def mark_read(self, item_id: int) -> None:
        await self._repository.mark_read(item_id)
