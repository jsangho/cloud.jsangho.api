from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from sangho.apps.titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from sangho.apps.titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from sangho.apps.titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from sangho.apps.titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from sangho.apps.titanic.dependencies.crew_walter_roaster_provider import get_walter_roaster
from sangho.apps.titanic.dependencies.passenger_cal_tester_provider import get_cal_tester
from sangho.apps.titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer
from sangho.apps.titanic.dependencies.passenger_rose_model_provider import get_rose_model
from titanic.adapter.outbound.pg.crew_smith_captain_pg_repository import SmithCaptainPgRepository
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository
from titanic.app.use_cases.crew_smith_captain_interactor import SmithCaptainInteractor

def get_smith_captain_repository(
    db: AsyncSession = Depends(get_db)
) -> SmithCaptainRepository:

    return SmithCaptainPgRepository(session=db)

def get_smith_captain(
        repository: SmithCaptainRepository = Depends(get_smith_captain_repository),
        jack: JackTrainerUseCase = Depends(get_jack_trainer),
        rose: RoseModelUseCase = Depends(get_rose_model),
        cal: CalTesterUseCase = Depends(get_cal_tester),
        walter: WalterRoasterUseCase = Depends(get_walter_roaster)
) -> SmithCaptainUseCase:

    return SmithCaptainInteractor(
        repository=repository,
        jack=jack,
        rose=rose,
        cal=cal,
        walter=walter
    )

