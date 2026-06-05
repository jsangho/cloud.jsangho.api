from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from kayfabe.adapter.outbound.pg.title_history_pg_repository import TitleHistoryPgRepository
from kayfabe.app.ports.input.title_history_use_case import TitleHistoryUseCase
from kayfabe.app.ports.output.title_history_repository import TitleHistoryRepository
from kayfabe.app.use_cases.title_history_interactor import TitleHistoryInteractor


def get_title_history_repository(
    db: AsyncSession = Depends(get_db),
) -> TitleHistoryRepository:
    return TitleHistoryPgRepository(db)


def get_title_history_use_case(
    db: AsyncSession = Depends(get_db),
) -> TitleHistoryUseCase:
    repository: TitleHistoryRepository = TitleHistoryPgRepository(db)
    return TitleHistoryInteractor(title_history_repository=repository)
