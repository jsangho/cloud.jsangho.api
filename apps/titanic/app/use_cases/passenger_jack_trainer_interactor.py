from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd

from titanic.adapter.outbound.orm.passenger_rose_model_strategies import build_all_strategies
from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.output.passenger_jack_trainer_port import JackTrainerPort

logger = logging.getLogger(__name__)


class JackTrainerInteractor:

    def __init__(self, repository: JackTrainerPort):
        self.repository = repository
        self._trained_strategies: dict = {}

    async def train_model(self, train_set: pd.DataFrame) -> dict[str, Any]:
        '''로즈가 제안한 모델들을 훈련시키는 메소드'''
        logger.info("[JackTrainerInteractor] 학습 파이프라인 시작")

        train = train_set.rename(columns={
            "survived":     "Survived",
            "name":         "Name",
            "sex":          "gender",
            "age":          "Age",
            "sibsp":        "SibSp",
            "parch":        "Parch",
            "fare":         "Fare",
            "cabin":        "Cabin",
            "embarked":     "Embarked",
            "passenger_id": "PassengerId",
            "pclass":       "Pclass",
        }).copy()

        # 수치형 컬럼 강제 변환 (ORM이 String으로 저장한 경우 대비)
        for col in ("Age", "SibSp", "Parch", "Fare"):
            if col in train.columns:
                train[col] = pd.to_numeric(train[col], errors="coerce")

        # 1. Label 분리
        y_label = train["Survived"].astype(int).tolist()
        train = train.drop("Survived", axis=1)

        # 2. 호칭 추출 및 Nominal 변환
        train["Title"] = train["Name"].str.extract(r"([A-Za-z]+)\.", expand=False)
        train["Title"] = train["Title"].replace(
            ["Capt", "Col", "Don", "Dr", "Major", "Rev", "Jonkheer", "Dona", "Mme"], "Rare"
        )
        train["Title"] = train["Title"].replace(["Countess", "Lady", "Sir"], "Royal")
        train["Title"] = train["Title"].replace({"Mlle": "Mr", "Ms": "Miss"})
        title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Royal": 5, "Rare": 6}
        train["Title"] = train["Title"].map(title_mapping).fillna(0).astype(int)

        # 3. 성별 Nominal 변환 (female=1, male=0)
        train["gender"] = train["gender"].map({"male": 0, "female": 1})

        # 4. 나이 구간 Ordinal 변환 및 결측치 처리
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf]
        age_labels = ["Unknown", "Baby", "Child", "Teenager", "Student", "Young Adult", "Adult", "Senior"]
        age_title_mapping = {
            0: "Unknown", 1: "Baby", 2: "Child", 3: "Teenager",
            4: "Student", 5: "Young Adult", 6: "Adult", 7: "Senior",
        }
        age_mapping = {v: k for k, v in age_title_mapping.items()}

        train["Age"] = train["Age"].fillna(-0.5)
        train["AgeGroup"] = pd.cut(train["Age"], bins, labels=age_labels).astype(str)
        mask = train["AgeGroup"] == "Unknown"
        train.loc[mask, "AgeGroup"] = train.loc[mask, "Title"].map(age_title_mapping)
        train["AgeGroup"] = train["AgeGroup"].map(age_mapping).fillna(0).astype(int)

        # 5. 승선항 Nominal 변환
        train["Embarked"] = train["Embarked"].fillna("S").map({"S": 1, "C": 2, "Q": 3})

        # 6. 요금 Ordinal 변환 (train 기준 4분위 구간 정의)
        train["FareBand"] = (
            pd.qcut(train["Fare"], 4, labels=[1, 2, 3, 4], duplicates="drop")
            .fillna(1).astype(int)
        )

        # 7. 불필요 컬럼 드롭
        drop_cols = ["Name", "Age", "Fare", "Ticket", "Cabin", "PassengerId"]
        train = train.drop(columns=[c for c in drop_cols if c in train.columns])

        X_train: list[list[float]] = train.values.tolist()

        # 8. 로즈의 10개 전략으로 학습
        self._trained_strategies = {}
        trained_names = []
        for key, StrategyClass in build_all_strategies().items():
            strategy = StrategyClass()
            try:
                strategy.fit(X_train, y_label)
                self._trained_strategies[key] = strategy
                trained_names.append(strategy.name)
                logger.info(f"[JackTrainerInteractor] {strategy.name} 학습 완료")
            except Exception as e:
                logger.warning(f"[JackTrainerInteractor] {key} 학습 실패 | error={e}")

        return {
            "train_samples": len(X_train),
            "trained_models": trained_names,
            "trained_strategies": self._trained_strategies,  # CalTesterInteractor에 전달
        }

    

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''잭 트레이너의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(JackTrainerQuery(
            id=schema.id,
            name=schema.name,
        ))