"""타이타닉 DB ORM·생존 예측 ML 모델."""

from __future__ import annotations

from sklearn.tree import DecisionTreeClassifier
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class PassengerModel(Base):
    """Neon Postgres 적재용 타이타닉 탑승자 ORM."""

    __tablename__ = "titanic_passengers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    passenger_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    survived: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pclass: Mapped[int | None] = mapped_column(Integer, nullable=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sex: Mapped[str | None] = mapped_column(String(10), nullable=True)
    age: Mapped[float | None] = mapped_column(Float, nullable=True)
    sibsp: Mapped[int | None] = mapped_column(Integer, nullable=True)
    parch: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ticket: Mapped[str | None] = mapped_column(String(64), nullable=True)
    fare: Mapped[float | None] = mapped_column(Float, nullable=True)
    cabin: Mapped[str | None] = mapped_column(String(32), nullable=True)
    embarked: Mapped[str | None] = mapped_column(String(1), nullable=True)

    def to_log_dict(self) -> dict:
        return {
            "id": self.id,
            "passenger_id": self.passenger_id,
            "survived": self.survived,
            "pclass": self.pclass,
            "sex": self.sex,
        }


class SurvivalModel:
    """생존 예측용 머신러닝 모델 (scikit-learn DecisionTree)."""

    def __init__(self) -> None:
        self.model = DecisionTreeClassifier()

    def get_model_name(self) -> str:
        return type(self.model).__name__

    @property
    def is_ready(self) -> bool:
        return self.model is not None
