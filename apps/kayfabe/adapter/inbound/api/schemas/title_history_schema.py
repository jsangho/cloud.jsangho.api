from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TitleAcquisitionSchema(BaseModel):
    belt_name: str = Field(alias="beltName")
    won_at: str = Field(alias="wonAt")
    won_at_slug: str | None = Field(default=None, alias="wonAtSlug")
    match_key: str | None = Field(default=None, alias="matchKey")

    model_config = ConfigDict(populate_by_name=True)


class CompetitorTitleHistoryResponseSchema(BaseModel):
    name: str
    acquisitions: list[TitleAcquisitionSchema]
    total: int

    model_config = ConfigDict(populate_by_name=True)
