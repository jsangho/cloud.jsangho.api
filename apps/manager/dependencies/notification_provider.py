from manager.adapter.outbound.n8n_notification_gateway import N8nNotificationGateway
from manager.app.ports.input.notification_use_case import NotificationUseCase
from manager.app.use_cases.notification_interactor import NotificationInteractor


def get_notification_use_case() -> NotificationUseCase:
    return NotificationInteractor(gateway=N8nNotificationGateway())
