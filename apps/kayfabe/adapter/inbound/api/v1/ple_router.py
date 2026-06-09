from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException

from kayfabe.adapter.outbound.mappers.ple_schema_mapper import (
    batch_prediction_from_schema,
    batch_results_from_schema,
    board_to_schema,
    event_sync_from_schema,
    match_result_update_from_schema,
    prediction_from_schema,
)
from kayfabe.adapter.inbound.api.schemas.ple_schema import (
    BatchPredictionRequestSchema,
    BatchResultsRequestSchema,
    LinkPredictionsSchema,
    MatchResultUpdateSchema,
    PleBoardSchema,
    PleEventSyncSchema,
    PredictionRequestSchema,
)
from kayfabe.app.exceptions import PleAuthRequiredError
from kayfabe.app.ports.input.ple_use_case import PleUseCase
from kayfabe.dependencies.ple_provider import get_ple_use_case

logger = logging.getLogger("uvicorn.error")

ple_router = APIRouter(prefix="/ple", tags=["ple"])


def _ple_http_error(exc: Exception) -> HTTPException:
    if isinstance(exc, LookupError):
        return HTTPException(status_code=404, detail=str(exc) or "Not found")
    if isinstance(exc, PleAuthRequiredError):
        return HTTPException(status_code=401, detail=str(exc) or "로그인이 필요합니다.")
    if isinstance(exc, ValueError):
        return HTTPException(status_code=400, detail=str(exc))
    raise exc


@ple_router.post(
    "/{slug}/sync-from-client",
    response_model=PleBoardSchema,
    response_model_by_alias=True,
)
async def sync_ple_from_client(
    slug: str,
    payload: PleEventSyncSchema,
    use_case: PleUseCase = Depends(get_ple_use_case),
):
    if payload.slug != slug:
        raise HTTPException(status_code=400, detail="URL slug와 본문 slug가 일치하지 않습니다.")
    logger.info(
        "[PleRouter] sync_ple_from_client | slug=%s matches=%d",
        slug,
        len(payload.matches),
    )
    try:
        board = await use_case.sync_event(payload=event_sync_from_schema(payload))
        return board_to_schema(board)
    except ValueError as e:
        raise _ple_http_error(e) from e


@ple_router.post("/link-predictions", response_model_by_alias=True)
async def link_ple_predictions(body: LinkPredictionsSchema):
    raise HTTPException(
        status_code=410,
        detail="예측은 로그인 후 저장됩니다. link-predictions API는 더 이상 사용하지 않습니다.",
    )


@ple_router.post(
    "/{slug}/predictions/batch",
    response_model=PleBoardSchema,
    response_model_by_alias=True,
)
async def predict_ple_batch(
    slug: str,
    body: BatchPredictionRequestSchema,
    use_case: PleUseCase = Depends(get_ple_use_case),
):
    logger.info("[PleRouter] predict_ple_batch | slug=%s count=%d", slug, len(body.predictions))
    try:
        board = await use_case.record_predictions_batch(
            slug=slug,
            body=batch_prediction_from_schema(body),
        )
        return board_to_schema(board)
    except (LookupError, ValueError, PleAuthRequiredError) as e:
        raise _ple_http_error(e) from e


@ple_router.post(
    "/{slug}/results/batch",
    response_model=PleBoardSchema,
    response_model_by_alias=True,
)
async def set_ple_results_batch(
    slug: str,
    body: BatchResultsRequestSchema,
    use_case: PleUseCase = Depends(get_ple_use_case),
):
    logger.info("[PleRouter] set_ple_results_batch | slug=%s count=%d", slug, len(body.results))
    try:
        board = await use_case.set_match_results_batch(
            slug=slug,
            body=batch_results_from_schema(body),
        )
        return board_to_schema(board)
    except (LookupError, ValueError) as e:
        raise _ple_http_error(e) from e


@ple_router.post(
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
    logger.info("[PleRouter] predict_ple_match | slug=%s match=%s", slug, match_key)
    try:
        board = await use_case.record_prediction(
            slug=slug,
            match_key=match_key,
            body=prediction_from_schema(body),
        )
        return board_to_schema(board)
    except (LookupError, ValueError, PleAuthRequiredError) as e:
        raise _ple_http_error(e) from e


@ple_router.post(
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
    logger.info("[PleRouter] set_ple_match_result | slug=%s match=%s", slug, match_key)
    try:
        board = await use_case.set_match_result(
            slug=slug,
            match_key=match_key,
            body=match_result_update_from_schema(body),
        )
        return board_to_schema(board)
    except (LookupError, ValueError) as e:
        raise _ple_http_error(e) from e
