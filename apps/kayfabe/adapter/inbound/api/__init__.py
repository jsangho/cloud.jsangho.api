from fastapi import APIRouter

from kayfabe.adapter.inbound.api.v1.ple_events_router import ple_events_router
from kayfabe.adapter.inbound.api.v1.ple_match_pick_router import (
    ple_match_pick_router,
    ranking_router,
)
from kayfabe.adapter.inbound.api.v1.ple_matches_router import (
    ple_matches_router,
    records_router,
)
from kayfabe.adapter.inbound.api.v1.title_acquisitions_router import (
    championship_router,
    title_acquisitions_router,
)

kayfabe_router = APIRouter(tags=["kayfabe"])
kayfabe_router.include_router(ple_events_router)
kayfabe_router.include_router(ple_match_pick_router)
kayfabe_router.include_router(ple_matches_router)
kayfabe_router.include_router(ranking_router)
kayfabe_router.include_router(records_router)
kayfabe_router.include_router(title_acquisitions_router)
kayfabe_router.include_router(championship_router)

__all__ = ["kayfabe_router"]
