from fastapi import APIRouter
from manager.adapter.inbound.api.v1.discord_router import discord_router
from manager.adapter.inbound.api.v1.juso_router import juso_router
from manager.adapter.inbound.api.v1.notification_router import notification_router
from manager.adapter.inbound.api.v1.telegram_router import telegram_router

manager_router = APIRouter(prefix="/manager", tags=["manager"])
manager_router.include_router(notification_router)
manager_router.include_router(discord_router)
manager_router.include_router(juso_router)
manager_router.include_router(telegram_router)

__all__ = ["manager_router"]
