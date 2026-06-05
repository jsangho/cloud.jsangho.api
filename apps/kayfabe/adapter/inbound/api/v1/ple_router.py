from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from kayfabe.adapter.inbound.api.schemas.ple_schema import (
    BatchPredictionRequestSchema,
    BatchResultsRequestSchema,
    LinkPredictionsSchema,
    MatchResultUpdateSchema,
    PleBoardSchema,
    PleEventSyncSchema,
    PredictionRequestSchema,
)
from kayfabe.app.ports.input.ple_use_case import PleUseCase
from kayfabe.app.exceptions import PleAuthRequiredError
from kayfabe.dependencies.ple import get_ple_use_case


ple_router = APIRouter(prefix="/ple", tags=["ple"])


def _ple_http_error(exc: Exception) -> HTTPException:
    if isinstance(exc, LookupError):
        return HTTPException(status_code=404, detail=str(exc) or "Not found")
    if isinstance(exc, PleAuthRequiredError):
        return HTTPException(status_code=401, detail=str(exc) or "ë¡ê·¸?¸ì´ ?ì?©ë??")
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
    """?ë¡ ??ë§¤ì¹ ì¹´ëë¥?Neon??upsert."""
    if payload.slug != slug:
        raise HTTPException(status_code=400, detail="URL slug? ë³¸ë¬¸ slugê° ?¼ì¹?ì? ?ìµ?ë¤.")
    try:
        return await use_case.sync_event(payload=payload)
    except ValueError as e:
        raise _ple_http_error(e) from e


@ple_router.post(
    "/link-predictions",
    response_model_by_alias=True,
)
async def link_ple_predictions(
    body: LinkPredictionsSchema,
):
    """(?ê±°?? ë¡ê·¸???ì ?ì±
 ?´í ? ê· ?ì¸¡?ë ?¬ì©?ì? ?ìµ?ë¤."""
    raise HTTPException(
        status_code=410,
        detail="?ì¸¡? ë¡ê·¸??????¥ë©?ë¤. link-predictions API?????´ì ?¬ì©?ì? ?ìµ?ë¤.",
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
    """ê²½ê¸° ?ì¸¡ ?¼ê´ ???"""
    try:
        return await use_case.record_predictions_batch(slug=slug, body=body)
    except (LookupError, ValueError) as e:
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
    """ê²½ê¸° ê²°ê³¼ ?¼ê´ ?±ë¡."""
    try:
        return await use_case.set_match_results_batch(slug=slug, body=body)
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
    """ê²½ê¸° ?ì¸¡ 1?????(Neon ple_predictions)."""
    try:
        return await use_case.record_prediction(slug=slug, match_key=match_key, body=body)
    except (LookupError, ValueError) as e:
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
    """ê²½ê¸° ê²°ê³¼ ?±ë¡Â·ê°±ì  (Neon ple_matches)."""
    try:
        return await use_case.set_match_result(slug=slug, match_key=match_key, body=body)
    except (LookupError, ValueError) as e:
        raise _ple_http_error(e) from e

