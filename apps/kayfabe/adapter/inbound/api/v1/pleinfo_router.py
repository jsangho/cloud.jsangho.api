from __future__ import annotations

import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse

from core.matrix.oracle_database import AsyncSessionLocal, rollback_readonly
from kayfabe.adapter.inbound.api.schemas.ple_schema import (
    PleAiStatsSchema,
    PleBoardSchema,
    PleEventSummarySchema,
)
from kayfabe.app.ports.input.pleinfo_use_case import PleInfoUseCase
from kayfabe.app.exceptions import PleAuthRequiredError
from kayfabe.dependencies.pleinfo import get_pleinfo_use_case


pleinfo_router = APIRouter(prefix="/ple", tags=["ple-info"])


def _ple_http_error(exc: Exception) -> HTTPException:
    if isinstance(exc, LookupError):
        return HTTPException(status_code=404, detail=str(exc) or "Not found")
    if isinstance(exc, PleAuthRequiredError):
        return HTTPException(status_code=401, detail=str(exc) or "ë¡ê·¸?¸ì´ ?ì?©ë??")
    if isinstance(exc, ValueError):
        return HTTPException(status_code=400, detail=str(exc))
    raise exc


@pleinfo_router.get(
    "/events",
    response_model=list[PleEventSummarySchema],
    response_model_by_alias=True,
)
async def list_ple_events(use_case: PleInfoUseCase = Depends(get_pleinfo_use_case)):
    """Neon???ê¸°?ë PLE ?´ë²¤??ëª©ë¡."""
    return await use_case.list_events()


@pleinfo_router.get(
    "/ai-stats",
    response_model=PleAiStatsSchema,
    response_model_by_alias=True,
)
async def get_ple_ai_stats(use_case: PleInfoUseCase = Depends(get_pleinfo_use_case)):
    """AI ?ì¸¡ ?ì  ?ì¤ë¥ Â·ìµê·?ì±ì  ê¸°ë¡."""
    return await use_case.get_ai_stats()


@pleinfo_router.get(
    "/{slug}",
    response_model=PleBoardSchema,
    response_model_by_alias=True,
)
async def get_ple_board(
    slug: str,
    client_id: str | None = None,
    user_id: int | None = None,
    use_case: PleInfoUseCase = Depends(get_pleinfo_use_case),
):
    """PLE ê²½ê¸° ë³´ë(ì¹´ëÂ·?¬ì´???¬íÂ·???ì¸¡)."""
    try:
        return await use_case.get_board(slug=slug, client_id=client_id, user_id=user_id)
    except LookupError as e:
        raise _ple_http_error(e) from e


@pleinfo_router.get("/{slug}/live")
async def ple_live_board(
    slug: str,
    client_id: str,
    request: Request,
    user_id: int | None = None,
):
    """ë³´ë ?¤ë
??SSE (?ì¸¡Â·ê²°ê³¼ ë°ì)."""

    async def event_stream():
        if AsyncSessionLocal is None:
            yield f"data: {json.dumps({'error': 'DATABASE_URL not configured'})}\n\n"
            return
        try:
            while True:
                if await request.is_disconnected():
                    return
                try:
                    async with AsyncSessionLocal() as session:
                        use_case = get_pleinfo_use_case(session)
                        board = await use_case.get_board(
                            slug=slug, client_id=client_id, user_id=user_id
                        )
                        await rollback_readonly(session)
                except LookupError as e:
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"
                    return
                except asyncio.CancelledError:
                    return
                payload = board.model_dump(mode="json", by_alias=True)
                yield f"data: {json.dumps(payload, default=str)}\n\n"
                try:
                    await asyncio.sleep(3)
                except asyncio.CancelledError:
                    return
        except asyncio.CancelledError:
            return

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )

