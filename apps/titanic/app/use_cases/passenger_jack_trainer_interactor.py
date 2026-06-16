from __future__ import annotations
from typing import Any

from kiwipiepy import Kiwi

from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository


class JackTrainerInteractor(JackTrainerUseCase):

    def __init__(self, repository: JackTrainerRepository, rose: RoseModelUseCase):
        self.repository = repository
        self.rose = rose
        self.kiwi = Kiwi()

    async def train_model(self, train_set) -> dict[str, Any]:
        """로즈가 제안한 모델들을 훈련시키는 메소드"""
        # ── 1. train_set 전처리 ───────────────────────────────────────────────
        df = train_set.copy()
        df["sex"] = (df["sex"] == "female").astype(float)
        df["embarked"] = df["embarked"].map({"S": 0.0, "C": 1.0, "Q": 2.0}).fillna(0.0)

        feature_cols = ["pclass", "sex", "age", "sibsp", "parch", "fare", "embarked"]
        mask = df[feature_cols + ["survived"]].notna().all(axis=1)
        X_train = df.loc[mask, feature_cols].values.tolist()
        y_train = df.loc[mask, "survived"].astype(int).tolist()

        # ── 2. 각 전략 훈련 (평가 없음 — 평가는 CalTesterInteractor에 위임) ────
        trained: list[str] = []
        failed:  list[dict[str, Any]] = []

        for algorithm in self.rose.list_algorithms():
            try:
                await self.rose.train(X_train, y_train, algorithm)
                trained.append(algorithm)
            except ImportError as e:
                failed.append({"algorithm": algorithm, "status": "skipped", "reason": f"패키지 미설치: {e}"})
            except Exception as e:
                failed.append({"algorithm": algorithm, "status": "error", "reason": str(e)})

        return {
            "train_samples": len(X_train),
            "features": feature_cols,
            "trained": trained,
            "failed": failed,
        }

    async def analyze_message_intent(self, user_message: str) -> dict:
        self.kiwi.global_config.space_tolerance = 2
        cleaned_text = self.kiwi.space(user_message, reset_whitespace=True)
        tokens = self.kiwi.tokenize(cleaned_text)
        keywords = [t.form for t in tokens if t.tag.startswith("NN")]
        return {"cleaned_text": cleaned_text, "keywords": keywords}

    async def introduce_myself(self, query: JackTrainerQuery) -> JackTrainerResponse:
        return await self.repository.introduce_myself(query)
