from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from kayfabe.adapter.outbound.pg.ple_pg_repository import PlePgRepository
from kayfabe.adapter.outbound.pg.pleinfo_pg_repository import PleInfoPgRepository
from kayfabe.app.ports.input.ple import PleUseCase
from kayfabe.app.ports.output.ple_repository import PleRepository
from kayfabe.app.ports.output.pleinfo_repository import PleInfoRepository
from kayfabe.app.use_cases.ple_interactor import PleInteractor


def get_ple(
    db: AsyncSession = Depends(get_db),
) -> PleUseCase:
    repository: PleRepository = PlePgRepository(db)
    info_repository: PleInfoRepository = PleInfoPgRepository(db)
    return PleInteractor(repository=repository, info_repository=info_repository)
