from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TitanicPassengerRowRequest(BaseModel):
    """
    CSV 1 row payload (all strings).

    Source columns (image):
    PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked

    - Sex column is mapped to `gender`.
    - All fields are `str` to keep inbound adapter simple.
    """

    model_config = ConfigDict(populate_by_name=True)

    passengerId: str = Field(alias="PassengerId")
    survived: str = Field(alias="Survived")
    pclass: str = Field(alias="Pclass")
    name: str = Field(alias="Name")
    gender: str = Field(alias="Sex")
    age: str = Field(alias="Age")
    sibSp: str = Field(alias="SibSp")
    parch: str = Field(alias="Parch")
    ticket: str = Field(alias="Ticket")
    fare: str = Field(alias="Fare")
    cabin: str = Field(alias="Cabin")
    embarked: str = Field(alias="Embarked")


class TitanicPassengersUpsertRequest(BaseModel):
    """Batch upsert request (CSV rows)."""

    model_config = ConfigDict(populate_by_name=True)

    rows: list[TitanicPassengerRowRequest] = Field(default_factory=list)

