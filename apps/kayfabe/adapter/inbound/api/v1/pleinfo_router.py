from __future__ import annotations

import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import AsyncSessionLocal, get_db, rollback_readonly
from kayfabe.app.ports.input.ple_schema import (
    PleAiStatsSchema,
    PleBoardSchema,
    PleEventSummarySchema,
)
from kayfabe.app.ports.input.pleinfo_use_case import PleInfoUseCase
from kayfabe.domain.exceptions import PleAuthRequiredError


router = APIRouter(prefix="/ple", tags=["ple-info"])


def _ple_http_error(exc: Exception) -> HTTPException:
    if isinstance(exc, LookupError):
        return HTTPException(status_code=404, detail=str(exc) or "Not found")
    if isinstance(exc, PleAuthRequiredError):
        return HTTPException(status_code=401, detail=str(exc) or "로그인이 필요합니다.")
    if isinstance(exc, ValueError):
        return HTTPException(status_code=400, detail=str(exc))
    raise exc


def get_pleinfo_use_case(db: AsyncSession = Depends(get_db)) -> PleInfoUseCase:
    from kayfabe.adapter.outbound.pg.pleinfo_pg_repository import PleInfoPgRepository
    from kayfabe.app.use_cases.pleinfo_interactor import PleInfoInteractor

    return PleInfoInteractor(PleInfoPgRepository(db))


@router.get(
    "/events",
    response_model=list[PleEventSummarySchema],
    response_model_by_alias=True,
)
async def list_ple_events(use_case: PleInfoUseCase = Depends(get_pleinfo_use_case)):
    """Neon에 동기화된 PLE 이벤트 목록."""
    return await use_case.list_events()


@router.get(
    "/ai-stats",
    response_model=PleAiStatsSchema,
    response_model_by_alias=True,
)
async def get_ple_ai_stats(use_case: PleInfoUseCase = Depends(get_pleinfo_use_case)):
    """AI 예측 누적 적중률·최근 채점 기록."""
    return await use_case.get_ai_stats()


@router.get(
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
    """PLE 경기 보드(카드·사이트 투표·내 예측)."""
    try:
        return await use_case.get_board(slug=slug, client_id=client_id, user_id=user_id)
    except LookupError as e:
        raise _ple_http_error(e) from e


@router.get("/{slug}/live")
async def ple_live_board(
    slug: str,
    client_id: str,
    request: Request,
    user_id: int | None = None,
):
    """보드 스냅샷 SSE (예측·결과 반영)."""

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

