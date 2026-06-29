from __future__ import annotations

from core.lol.t1_mid_faker_orchestrator import FakerOrchestrator

from manager.app.dtos.notification_dto import NotificationDto
from manager.app.ports.input.notification_use_case import NotificationUseCase
from manager.app.ports.output.notification_gateway import NotificationGateway

_FAKER_PROMPT = (
    "T1 미드라이너 이상혁(페이커)의 플레이 스타일, 대표 챔피언, "
    "최근 시즌 활약상을 분석하는 보고서를 한국어로 작성해주세요. "
    "3~4 문단으로 구성해주세요."
)
_SUBJECT = "[T1] 페이커 미드라이너 활약 보고서"


class NotificationInteractor(NotificationUseCase):
    def __init__(self, gateway: NotificationGateway) -> None:
        self._gateway = gateway
        self._orchestrator = FakerOrchestrator()

    async def send_faker_report(self, to: str) -> dict:
        body = await self._orchestrator.generate(_FAKER_PROMPT)
        await self._gateway.send(NotificationDto(to=to, subject=_SUBJECT, body=body))
        return {"status": "sent", "to": to}
