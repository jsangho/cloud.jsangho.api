from fastapi import APIRouter

from kayfabe.adapter.inbound.api.v1.ple_router import ple_router
from kayfabe.adapter.inbound.api.v1.pleinfo_router import pleinfo_router
from kayfabe.adapter.inbound.api.v1.ranking_router import ranking_router
from kayfabe.adapter.inbound.api.v1.records_router import records_router
from kayfabe.adapter.inbound.api.v1.result_router import result_router
from kayfabe.adapter.inbound.api.v1.title_history_router import title_history_router

kayfabe_router = APIRouter(tags=["kayfabe"])
kayfabe_router.include_router(ple_router)
kayfabe_router.include_router(pleinfo_router)
kayfabe_router.include_router(ranking_router)
kayfabe_router.include_router(records_router)
kayfabe_router.include_router(title_history_router)
kayfabe_router.include_router(result_router)

__all__ = ["kayfabe_router"]
