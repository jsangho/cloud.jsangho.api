from fastapi import APIRouter
from manager.adapter.inbound.api.v1.discord_router import discord_router
from manager.adapter.inbound.api.v1.email_router import email_router
from manager.adapter.inbound.api.v1.juso_router import juso_router
from manager.adapter.inbound.api.v1.received_router import inbox_router
from manager.adapter.inbound.api.v1.telegram_router import telegram_router

manager_router = APIRouter(prefix="/manager", tags=["manager"])
manager_router.include_router(email_router)
manager_router.include_router(discord_router)
manager_router.include_router(juso_router)
manager_router.include_router(telegram_router)
manager_router.include_router(inbox_router)

__all__ = ["manager_router"]
