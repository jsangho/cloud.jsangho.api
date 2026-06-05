from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from kayfabe.adapter.outbound.pg.pleinfo_pg_repository import PleInfoPgRepository
from kayfabe.app.ports.input.pleinfo_use_case import PleInfoUseCase
from kayfabe.app.ports.output.pleinfo_repository import PleInfoRepository
from kayfabe.app.use_cases.pleinfo_interactor import PleInfoInteractor


def get_pleinfo_use_case(
    db: AsyncSession = Depends(get_db),
) -> PleInfoUseCase:
    repository: PleInfoRepository = PleInfoPgRepository(db)
    return PleInfoInteractor(repository=repository)
