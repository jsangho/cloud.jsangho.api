from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from kayfabe.adapter.outbound.pg.ple_events_pg_repository import (
    PleInfoPgRepository,
    PleMyselfPgRepository,
    PlePgRepository,
)
from kayfabe.app.dtos.myself_dto import MyselfRepository, MyselfUseCase
from kayfabe.app.ports.input.ple_events_use_case import PleInfoUseCase, PleUseCase
from kayfabe.app.ports.output.ple_events_repository import PleInfoRepository, PleRepository
from kayfabe.app.use_cases.ple_events_interactor import (
    PleInfoInteractor,
    PleInteractor,
    PleMyselfInteractor,
)


def get_pleinfo_repository(
    db: AsyncSession = Depends(get_db),
) -> PleInfoRepository:
    return PleInfoPgRepository(db)


def get_pleinfo(
    repository: PleInfoRepository = Depends(get_pleinfo_repository),
) -> PleInfoUseCase:
    return PleInfoInteractor(repository=repository)


def get_ple_repository(
    db: AsyncSession = Depends(get_db),
) -> PleRepository:
    return PlePgRepository(db)


def get_ple(
    repository: PleRepository = Depends(get_ple_repository),
    info_use_case: PleInfoUseCase = Depends(get_pleinfo),
) -> PleUseCase:
    return PleInteractor(repository=repository, info_use_case=info_use_case)


def get_ple_myself_repository(
    db: AsyncSession = Depends(get_db),
) -> MyselfRepository:
    return PleMyselfPgRepository(session=db)


def get_ple_myself(
    repository: MyselfRepository = Depends(get_ple_myself_repository),
) -> MyselfUseCase:
    return PleMyselfInteractor(repository=repository)
