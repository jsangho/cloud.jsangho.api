from kayfabe.adapter.outbound.catalog.current_championship_catalog_repository import (
    CurrentChampionshipCatalogRepository,
)
from kayfabe.app.ports.input.championship import ChampionshipUseCase
from kayfabe.app.ports.output.championship_repository import ChampionshipRepository
from kayfabe.app.use_cases.championship_interactor import ChampionshipInteractor


def get_championship() -> ChampionshipUseCase:
    repository: ChampionshipRepository = CurrentChampionshipCatalogRepository()
    return ChampionshipInteractor(championship_repository=repository)
