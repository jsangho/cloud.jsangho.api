from fastapi import APIRouter, Depends
from manager.adapter.inbound.api.shemas.telegram_schema import TelegramMyselfSchema
from manager.app.dtos.telegram_dto import TelegramQuery, TelegramResponse
from manager.app.ports.input.telegram_use_case import TelegramUseCase
from manager.dependencies.telegram_provider import get_telegram_use_case

telegram_router = APIRouter(prefix="/telegram", tags=["telegram"])


@telegram_router.get("/myself")
async def introduce_myself(
    use_case: TelegramUseCase = Depends(get_telegram_use_case),
) -> TelegramResponse:
    schema = TelegramMyselfSchema()
    query = TelegramQuery(id=schema.id, name=schema.name)
    return await use_case.introduce_myself(query)
