from fastapi import APIRouter
from manager.adapter.inbound.api.v1.notification_router import notification_router

manager_router = APIRouter(prefix="/manager", tags=["manager"])
manager_router.include_router(notification_router)

__all__ = ["manager_router"]
