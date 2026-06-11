from __future__ import annotations

import asyncio
import json
import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse

from core.matrix.grid_oracle_database_manager import AsyncSessionLocal, rollback_readonly
from kayfabe.adapter.outbound.mappers.ple_schema_mapper import (
    ai_stats_to_schema,
    board_to_schema,
    event_summary_to_schema,
)
from kayfabe.adapter.inbound.api.schemas.ple_schema import (
    PleAiStatsSchema,
    PleBoardSchema,
    PleEventSummarySchema,
)
from kayfabe.app.exceptions import PleAuthRequiredError
from kayfabe.app.ports.input.pleinfo import PleInfoUseCase
from kayfabe.dependencies.pleinfo_provider import get_pleinfo

logger = logging.getLogger("uvicorn.error")

pleinfo_router = APIRouter(prefix="/ple", tags=["ple-info"])


def _ple_http_error(exc: Exception) -> HTTPException:
    if isinstance(exc, LookupError):
        return HTTPException(status_code=404, detail=str(exc) or "Not found")
    if isinstance(exc, PleAuthRequiredError):
        return HTTPException(status_code=401, detail=str(exc) or "로그인이 필요합니다.")
    if isinstance(exc, ValueError):
        return HTTPException(status_code=400, detail=str(exc))
    raise exc


@pleinfo_router.get(
    "/events",
    response_model=list[PleEventSummarySchema],
    response_model_by_alias=True,
)
async def list_ple_events(use_case: PleInfoUseCase = Depends(get_pleinfo)):
    logger.info("[PleInfoRouter] list_ple_events")
    events = await use_case.list_events()
    return [event_summary_to_schema(e) for e in events]


@pleinfo_router.get(
    "/ai-stats",
    response_model=PleAiStatsSchema,
    response_model_by_alias=True,
)
async def get_ple_ai_stats(use_case: PleInfoUseCase = Depends(get_pleinfo)):
    logger.info("[PleInfoRouter] get_ple_ai_stats")
    return ai_stats_to_schema(await use_case.get_ai_stats())


@pleinfo_router.get(
    "/{slug}",
    response_model=PleBoardSchema,
    response_model_by_alias=True,
)
async def get_ple_board(
    slug: str,
    client_id: str | None = None,
    user_id: int | None = None,
    use_case: PleInfoUseCase = Depends(get_pleinfo),
):
    logger.info("[PleInfoRouter] get_ple_board | slug=%s", slug)
    try:
        return board_to_schema(
            await use_case.get_board(slug=slug, client_id=client_id, user_id=user_id)
        )
    except LookupError as e:
        raise _ple_http_error(e) from e


@pleinfo_router.get("/{slug}/live")
async def ple_live_board(
    slug: str,
    client_id: str,
    request: Request,
    user_id: int | None = None,
):
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
                        use_case = get_pleinfo(session)
                        board = await use_case.get_board(
                            slug=slug, client_id=client_id, user_id=user_id
                        )
                        await rollback_readonly(session)
                except LookupError as e:
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"
                    return
                except asyncio.CancelledError:
                    return
                payload = board_to_schema(board).model_dump(mode="json", by_alias=True)
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
