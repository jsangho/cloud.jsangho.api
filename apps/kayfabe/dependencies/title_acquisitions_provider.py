from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from kayfabe.adapter.outbound.catalog.current_championship_catalog_repository import (
    CurrentChampionshipCatalogRepository,
)
from kayfabe.adapter.outbound.pg.title_acquisitions_pg_repository import (
    ChampionshipMyselfPgRepository,
    TitleHistoryMyselfPgRepository,
    TitleHistoryPgRepository,
)
from kayfabe.app.dtos.myself_dto import MyselfRepository, MyselfUseCase
from kayfabe.app.ports.input.title_acquisitions_use_case import ChampionshipUseCase, TitleHistoryUseCase
from kayfabe.app.ports.output.title_acquisitions_repository import (
    ChampionshipRepository,
    TitleHistoryRepository,
)
from kayfabe.app.use_cases.title_acquisitions_interactor import (
    ChampionshipInteractor,
    ChampionshipMyselfInteractor,
    TitleHistoryInteractor,
    TitleHistoryMyselfInteractor,
)


def get_title_history_repository(
    db: AsyncSession = Depends(get_db),
) -> TitleHistoryRepository:
    return TitleHistoryPgRepository(db)


def get_title_history(
    repository: TitleHistoryRepository = Depends(get_title_history_repository),
) -> TitleHistoryUseCase:
    return TitleHistoryInteractor(title_history_repository=repository)


def get_championship_repository() -> ChampionshipRepository:
    return CurrentChampionshipCatalogRepository()


def get_championship(
    repository: ChampionshipRepository = Depends(get_championship_repository),
) -> ChampionshipUseCase:
    return ChampionshipInteractor(championship_repository=repository)


def get_title_history_myself_repository(
    db: AsyncSession = Depends(get_db),
) -> MyselfRepository:
    return TitleHistoryMyselfPgRepository(session=db)


def get_title_history_myself(
    repository: MyselfRepository = Depends(get_title_history_myself_repository),
) -> MyselfUseCase:
    return TitleHistoryMyselfInteractor(repository=repository)


def get_championship_myself_repository(
    db: AsyncSession = Depends(get_db),
) -> MyselfRepository:
    return ChampionshipMyselfPgRepository(session=db)


def get_championship_myself(
    repository: MyselfRepository = Depends(get_championship_myself_repository),
) -> MyselfUseCase:
    return ChampionshipMyselfInteractor(repository=repository)
