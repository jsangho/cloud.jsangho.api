from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from kayfabe.adapter.outbound.pg.pleinfo_pg_repository import PleInfoPgRepository
from kayfabe.app.ports.input.pleinfo import PleInfoUseCase
from kayfabe.app.ports.output.pleinfo_repository import PleInfoRepository
from kayfabe.app.use_cases.pleinfo_interactor import PleInfoInteractor


def get_pleinfo(
    db: AsyncSession = Depends(get_db),
) -> PleInfoUseCase:
    repository: PleInfoRepository = PleInfoPgRepository(db)
    return PleInfoInteractor(repository=repository)
