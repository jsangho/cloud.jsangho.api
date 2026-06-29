from fastapi import APIRouter, Depends
from manager.adapter.inbound.api.shemas.notification_schema import NotifyRequest
from manager.app.ports.input.notification_use_case import NotificationUseCase
from manager.dependencies.notification_provider import get_notification_use_case

notification_router = APIRouter(prefix="/notify", tags=["notify"])


@notification_router.post("/faker-report")
async def send_faker_report(
    body: NotifyRequest,
    use_case: NotificationUseCase = Depends(get_notification_use_case),
) -> dict:
    return await use_case.send_faker_report(to=body.to)
