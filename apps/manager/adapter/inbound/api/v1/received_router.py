from __future__ import annotations

from fastapi import APIRouter, Depends
from manager.adapter.inbound.api.schemas.received_schema import (
    ReceivedResponse,
    ReceiveRequest,
)
from manager.app.dtos.received_dto import ReceivedCommand
from manager.app.ports.input.received_use_case import ReceivedUseCase
from manager.dependencies.received_provider import get_received_use_case

inbox_router = APIRouter(prefix="/inbox", tags=["inbox"])


@inbox_router.post("/receive", summary="n8n → 수신 데이터 저장")
async def receive(
    body: ReceiveRequest,
    use_case: ReceivedUseCase = Depends(get_received_use_case),
) -> dict[str, int]:
    cmd = ReceivedCommand(
        from_email=body.from_email,
        from_name=body.from_name,
        to_email=body.to_email,
        subject=body.subject,
        body=body.body,
        message_id=body.message_id,
    )
    return await use_case.receive(cmd)


@inbox_router.get("/list", summary="받은편지함 목록 조회")
async def list_inbox(
    use_case: ReceivedUseCase = Depends(get_received_use_case),
) -> list[ReceivedResponse]:
    items = await use_case.list_inbox()
    return [
        ReceivedResponse(
            id=item.id,
            from_email=item.from_email,
            from_name=item.from_name,
            to_email=item.to_email,
            subject=item.subject,
            body=item.body,
            message_id=item.message_id,
            received_at=item.received_at,
            is_read=item.is_read,
        )
        for item in items
    ]


@inbox_router.patch("/{item_id}/read", summary="읽음 처리")
async def mark_read(
    item_id: int,
    use_case: ReceivedUseCase = Depends(get_received_use_case),
) -> dict[str, str]:
    await use_case.mark_read(item_id)
    return {"status": "ok"}
