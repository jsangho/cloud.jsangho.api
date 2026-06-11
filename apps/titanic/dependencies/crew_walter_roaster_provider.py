from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from titanic.adapter.outbound.pg.crew_walter_roaster_pg_repository import WalterRoasterPgRepository
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.output.crew_walter_roaster_repository import WalterRoasterRepository
from titanic.app.use_cases.crew_walter_roaster_interactor import WalterRoasterInteractor


def get_walter_roaster(
    db: AsyncSession = Depends(get_db),
) -> WalterRoasterUseCase:
    repository: WalterRoasterRepository = WalterRoasterPgRepository(session=db)
    return WalterRoasterInteractor(repository=repository)

get_walter_roaster_use_case = get_walter_roaster
