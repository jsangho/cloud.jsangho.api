from __future__ import annotations

from manager.adapter.outbound.repositories.received_repository import (
    ReceivedPgRepository,
)
from manager.app.ports.input.received_use_case import ReceivedUseCase
from manager.app.use_cases.received_interactor import ReceivedInteractor


def get_received_use_case() -> ReceivedUseCase:
    return ReceivedInteractor(ReceivedPgRepository())
