from fastapi import APIRouter

from friday13th.adapter.inbound.api.v1.jason_mask_router import jason_mask_router
from friday13th.adapter.inbound.api.v1.murder_list_router import murder_list_router
from friday13th.adapter.inbound.api.v1.pamela_cook_router import pamela_cook_router

friday13th_router = APIRouter(prefix="/friday13th", tags=["friday13th"])
friday13th_router.include_router(jason_mask_router)
friday13th_router.include_router(pamela_cook_router)
friday13th_router.include_router(murder_list_router)

__all__ = ["friday13th_router"]
