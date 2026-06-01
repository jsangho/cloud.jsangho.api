from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from kayfabe.app.ports.input.ple_schema import (
    BatchPredictionRequestSchema,
    BatchResultsRequestSchema,
    LinkPredictionsSchema,
    MatchResultUpdateSchema,
    PleBoardSchema,
    PleEventSyncSchema,
    PredictionRequestSchema,
)
from kayfabe.app.ports.input.ple_use_case import PleUseCase
from kayfabe.domain.exceptions import PleAuthRequiredError


router = APIRouter(prefix="/ple", tags=["ple"])


def _ple_http_error(exc: Exception) -> HTTPException:
    if isinstance(exc, LookupError):
        return HTTPException(status_code=404, detail=str(exc) or "Not found")
    if isinstance(exc, PleAuthRequiredError):
        return HTTPException(status_code=401, detail=str(exc) or "로그인이 필요합니다.")
    if isinstance(exc, ValueError):
        return HTTPException(status_code=400, detail=str(exc))
    raise exc


def get_ple_use_case(db: AsyncSession = Depends(get_db)) -> PleUseCase:
    from kayfabe.adapter.outbound.pg.ple_pg_repository import PlePgRepository
    from kayfabe.adapter.outbound.pg.pleinfo_pg_repository import PleInfoPgRepository
    from kayfabe.app.use_cases.ple_interactor import PleInteractor

    return PleInteractor(PlePgRepository(db), PleInfoPgRepository(db))


@router.post(
    "/{slug}/sync-from-client",
    response_model=PleBoardSchema,
    response_model_by_alias=True,
)
async def sync_ple_from_client(
    slug: str,
    payload: PleEventSyncSchema,
    use_case: PleUseCase = Depends(get_ple_use_case),
):
    """프론트 매치 카드를 Neon에 upsert."""
    if payload.slug != slug:
        raise HTTPException(status_code=400, detail="URL slug와 본문 slug가 일치하지 않습니다.")
    try:
        return await use_case.sync_event(payload=payload)
    except ValueError as e:
        raise _ple_http_error(e) from e


@router.post(
    "/link-predictions",
    response_model_by_alias=True,
)
async def link_ple_predictions(
    body: LinkPredictionsSchema,
):
    """(레거시) 로그인 필수 정책 이후 신규 예측에는 사용하지 않습니다."""
    raise HTTPException(
        status_code=410,
        detail="예측은 로그인 후 저장됩니다. link-predictions API는 더 이상 사용하지 않습니다.",
    )


@router.post(
    "/{slug}/predictions/batch",
    response_model=PleBoardSchema,
    response_model_by_alias=True,
)
async def predict_ple_batch(
    slug: str,
    body: BatchPredictionRequestSchema,
    use_case: PleUseCase = Depends(get_ple_use_case),
):
    """경기 예측 일괄 저장."""
    try:
        return await use_case.record_predictions_batch(slug=slug, body=body)
    except (LookupError, ValueError) as e:
        raise _ple_http_error(e) from e


@router.post(
    "/{slug}/results/batch",
    response_model=PleBoardSchema,
    response_model_by_alias=True,
)
async def set_ple_results_batch(
    slug: str,
    body: BatchResultsRequestSchema,
    use_case: PleUseCase = Depends(get_ple_use_case),
):
    """경기 결과 일괄 등록."""
    try:
        return await use_case.set_match_results_batch(slug=slug, body=body)
    except (LookupError, ValueError) as e:
        raise _ple_http_error(e) from e


@router.post(
    "/{slug}/matches/{match_key}/predict",
    response_model=PleBoardSchema,
    response_model_by_alias=True,
)
async def predict_ple_match(
    slug: str,
    match_key: str,
    body: PredictionRequestSchema,
    use_case: PleUseCase = Depends(get_ple_use_case),
):
    """경기 예측 1회 저장 (Neon ple_predictions)."""
    try:
        return await use_case.record_prediction(slug=slug, match_key=match_key, body=body)
    except (LookupError, ValueError) as e:
        raise _ple_http_error(e) from e


@router.post(
    "/{slug}/matches/{match_key}/result",
    response_model=PleBoardSchema,
    response_model_by_alias=True,
)
async def set_ple_match_result(
    slug: str,
    match_key: str,
    body: MatchResultUpdateSchema,
    use_case: PleUseCase = Depends(get_ple_use_case),
):
    """경기 결과 등록·갱신 (Neon ple_matches)."""
    try:
        return await use_case.set_match_result(slug=slug, match_key=match_key, body=body)
    except (LookupError, ValueError) as e:
        raise _ple_http_error(e) from e

