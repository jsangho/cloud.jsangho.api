from __future__ import annotations

from kayfabe.app.dtos.championship_dto import (
    BrandRosterDto,
    ChampionshipBoardDto,
    TitleReignDto,
)
from kayfabe.app.ports.output.championship_repository import ChampionshipRepository
from kayfabe.app.services.current_championship_catalog import (
    CHAMPIONSHIP_AS_OF,
    WWE_BRAND_CHAMPIONS,
)


class CurrentChampionshipCatalogRepository(ChampionshipRepository):
    async def get_board(self) -> ChampionshipBoardDto:
        brands = [
            BrandRosterDto(
                id=brand["id"],
                label=brand["label"],
                tagline=brand["tagline"],
                accent=brand["accent"],
                titles=[
                    TitleReignDto(
                        belt_name=title["belt_name"],
                        champions=list(title["champions"]),
                        team_name=title.get("team_name"),
                        won_at=title["won_at"],
                        won_event=title.get("won_event"),
                        tier=title["tier"],
                    )
                    for title in brand["titles"]
                ],
            )
            for brand in WWE_BRAND_CHAMPIONS
        ]
        return ChampionshipBoardDto(as_of=CHAMPIONSHIP_AS_OF, brands=brands)
