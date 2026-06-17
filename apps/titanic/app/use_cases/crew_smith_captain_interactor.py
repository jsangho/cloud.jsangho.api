from __future__ import annotations

import logging

import numpy as np
import pandas as pd
from pandas import DataFrame

from titanic.app.dtos.crew_smith_captain_dto import (
    SmithCaptainChatCommand,
    SmithCaptainQuery,
    SmithCaptainResponse,
)
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.crew_smith_captain_port import SmithCaptainPort

logger = logging.getLogger(__name__)

_AGE_GROUPS: list[tuple[str, float, float]] = [
    ("영아(0-4)",       0,   5),
    ("아동(5-11)",      5,  12),
    ("청소년(12-17)",  12,  18),
    ("청년(18-23)",    18,  24),
    ("젊은성인(24-34)", 24,  35),
    ("성인(35-59)",    35,  60),
    ("노인(60+)",      60, 200),
]


class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(
        self,
        repository: SmithCaptainPort,
        andrews: AndrewsArchitectUseCase,
        jack: JackTrainerUseCase,
        rose: RoseModelUseCase,
        cal: CalTesterUseCase,
        walter: WalterRoasterUseCase,
    ):
        self.repository = repository
        self.andrews = andrews
        self.jack = jack
        self.rose = rose
        self.cal = cal
        self.walter = walter

    # ── 필터 감지 ─────────────────────────────────────────────────────────────

    @staticmethod
    def _detect_pclass(text: str) -> str | None:
        if any(k in text for k in ("1등석", "1등급", "일등석", "퍼스트")):
            return "1"
        if any(k in text for k in ("2등석", "2등급", "이등석", "세컨드")):
            return "2"
        if any(k in text for k in ("3등석", "3등급", "삼등석", "서드")):
            return "3"
        return None

    @staticmethod
    def _detect_age_range(text: str) -> tuple[float, float] | None:
        candidates: list[tuple[str, float, float]] = [
            ("영아",   0,  5), ("아기",   0,  5), ("유아",   0,  5),
            ("아동",   5, 12), ("어린이", 5, 12),
            ("청소년", 12, 18),
            ("10대",   10, 20),
            ("20대",   20, 30),
            ("30대",   30, 40),
            ("40대",   40, 50),
            ("50대",   50, 60),
            ("60대",   60, 200), ("노인", 60, 200), ("고령", 60, 200),
        ]
        for label, lo, hi in candidates:
            if label in text:
                return (lo, hi)
        return None

    @staticmethod
    def _detect_sex(text: str) -> str | None:
        if any(k in text for k in ("여성", "여자", "여아")):
            return "female"
        if any(k in text for k in ("남성", "남자", "남아")):
            return "male"
        return None

    @staticmethod
    def _age_range_label(age_range: tuple[float, float]) -> str:
        mapping = {
            (0,   5):  "영아(0-4세)",   (5,  12): "아동(5-11세)",
            (12, 18):  "청소년(12-17세)", (10, 20): "10대",
            (20, 30):  "20대",           (30, 40): "30대",
            (40, 50):  "40대",           (50, 60): "50대",
            (60, 200): "60대 이상",
        }
        lo, hi = age_range
        return mapping.get((lo, hi), f"{int(lo)}-{int(hi)}세")

    # ── 전처리 헬퍼 (JackTrainer와 동일한 파이프라인) ─────────────────────────

    def _preprocess_df(self, df: DataFrame) -> list[list]:
        data = df.rename(columns={
            "name": "Name", "sex": "gender", "age": "Age",
            "sibsp": "SibSp", "parch": "Parch", "fare": "Fare",
            "cabin": "Cabin", "embarked": "Embarked",
            "passenger_id": "PassengerId", "pclass": "Pclass",
        }).copy()
        for col in ("Age", "SibSp", "Parch", "Fare"):
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors="coerce")
        data["Title"] = data["Name"].str.extract(r"([A-Za-z]+)\.", expand=False)
        data["Title"] = (
            data["Title"]
            .replace(["Capt","Col","Don","Dr","Major","Rev","Jonkheer","Dona","Mme"], "Rare")
            .replace(["Countess","Lady","Sir"], "Royal")
            .replace({"Mlle": "Mr", "Ms": "Miss"})
        )
        data["Title"] = data["Title"].map(
            {"Mr":1,"Miss":2,"Mrs":3,"Master":4,"Royal":5,"Rare":6}
        ).fillna(0).astype(int)
        data["gender"] = data["gender"].map({"male":0,"female":1}).fillna(0).astype(int)
        age_title_map = {0:"Unknown",1:"Baby",2:"Child",3:"Teenager",
                         4:"Student",5:"Young Adult",6:"Adult",7:"Senior"}
        age_map = {v:k for k,v in age_title_map.items()}
        data["Age"] = data["Age"].fillna(-0.5)
        data["AgeGroup"] = pd.cut(data["Age"], [-1,0,5,12,18,24,35,60,np.inf],
                                  labels=list(age_title_map.values())).astype(str)
        mask = data["AgeGroup"] == "Unknown"
        data.loc[mask, "AgeGroup"] = data.loc[mask, "Title"].map(age_title_map)
        data["AgeGroup"] = data["AgeGroup"].map(age_map).fillna(0).astype(int)
        data["Embarked"] = data["Embarked"].fillna("S").map({"S":1,"C":2,"Q":3}).fillna(1).astype(int)
        data["Fare"] = data["Fare"].fillna(data["Fare"].median())
        try:
            data["FareBand"] = (
                pd.qcut(data["Fare"], 4, labels=[1,2,3,4], duplicates="drop")
                .fillna(1).astype(int)
            )
        except Exception:
            data["FareBand"] = 1
        data = data.drop(columns=[c for c in ["Name","Age","Fare","Ticket","Cabin","PassengerId"]
                                   if c in data.columns])
        return data.values.tolist()

    # ── 80/20 홀드아웃으로 최적 모델 선택 → test_set 전체 예측 ─────────────────

    async def _predict_test_survival(
        self, train_set: DataFrame, test_set: DataFrame
    ) -> tuple[str, list[int]]:
        from sklearn.metrics import f1_score as sk_f1

        n = len(train_set)
        split = int(n * 0.8)
        t_df = train_set.iloc[:split].copy()
        v_df = train_set.iloc[split:].copy()
        y_val = pd.to_numeric(v_df["survived"], errors="coerce").fillna(0).astype(int).tolist()
        v_features = v_df.drop(columns=["survived"], errors="ignore")
        train_result = await self.jack.train_model(t_df)
        trained: dict = train_result.get("trained_strategies", {})
        X_val = self._preprocess_df(v_features)

        best_name, best_strategy, best_f1 = "unknown", None, -1.0
        for name, strategy in trained.items():
            try:
                score = sk_f1(y_val, strategy.predict(X_val), zero_division=0)
                if score > best_f1:
                    best_f1, best_name, best_strategy = score, name, strategy
            except Exception:
                pass

        if best_strategy is None:
            return "unknown", [0] * len(test_set)
        logger.info(f"[SmithCaptainInteractor] 최적 모델={best_name} val_f1={best_f1:.4f}")
        return best_name, best_strategy.predict(self._preprocess_df(test_set))

    # ── 예측 포함 test_set 반환 ───────────────────────────────────────────────

    async def _with_predictions(
        self, train_set: DataFrame, test_set: DataFrame
    ) -> tuple[str, DataFrame]:
        best_name, predictions = await self._predict_test_survival(train_set, test_set)
        test_copy = test_set.copy()
        test_copy["survived_pred"] = predictions
        return best_name, test_copy

    # ── 생존/사망 통계 계산 ────────────────────────────────────────────────────

    @staticmethod
    def _stats(train_f: DataFrame, test_f: DataFrame) -> tuple[int, int, int]:
        """(total, survived, dead) 반환"""
        s = int(pd.to_numeric(train_f["survived"], errors="coerce").fillna(0).sum())
        s += int(test_f["survived_pred"].sum()) if "survived_pred" in test_f.columns else 0
        total = len(train_f) + len(test_f)
        return total, s, total - s

    @staticmethod
    def _surv_lines(total: int, survived: int, dead: int, best_name: str) -> str:
        return (
            f"• 생존자: 약 {survived}명 ({survived/total:.1%})\n"
            f"• 사망자: 약 {dead}명 ({dead/total:.1%})\n"
            f"(예측 포함 [{best_name}])"
        )

    # ── 데이터프레임 필터 적용 ────────────────────────────────────────────────

    @staticmethod
    def _apply_filters(
        df: DataFrame,
        pclass: str | None = None,
        age_range: tuple[float, float] | None = None,
        sex: str | None = None,
    ) -> DataFrame:
        r = df.copy()
        if pclass:
            r = r[r["pclass"].astype(str) == pclass]
        if age_range:
            lo, hi = age_range
            a = pd.to_numeric(r["age"], errors="coerce")
            r = r[(a >= lo) & (a < hi)]
        if sex:
            r = r[r["sex"] == sex]
        return r

    # ── 채팅 메인 ────────────────────────────────────────────────────────────

    async def chat(self, command: SmithCaptainChatCommand) -> str:
        user_text = command.messages[-1].text if command.messages else ""
        logger.info(f"[SmithCaptainInteractor] chat 진입 | messages={user_text}")

        question: dict = self.andrews.analyze_intent(user_text)
        intent = question.get("intent", "UNKNOWN")
        logger.info(f"[SmithCaptainInteractor] intent={intent}")

        # ── ML 모델 학습/평가 ─────────────────────────────────────────────────
        if intent == "MODEL_TRAIN":
            train_set: DataFrame = await self.walter.get_train_set()
            test_set: DataFrame  = await self.walter.get_test_set()
            train_result = await self.jack.train_model(train_set)
            test_result  = await self.cal.test_model(test_set)
            rankings = [r for r in test_result.get("rankings", []) if r.get("status") == "success"]
            if not rankings:
                trained = train_result.get("trained_models", [])
                return f"모델 학습을 완료했습니다. ({len(trained)}개)\n평가용 레이블 데이터가 없어 정확도는 측정할 수 없습니다."
            best = min(rankings, key=lambda r: r.get("rank", 999))
            return (
                f"가장 정확한 알고리즘은 '{best['algorithm']}'입니다.\n"
                f"• 정확도(Accuracy): {best['accuracy']:.2%}\n"
                f"• F1 Score: {best['f1']:.4f}"
            )

        # ── 필터 감지 ─────────────────────────────────────────────────────────
        pclass    = self._detect_pclass(user_text)
        age_range = self._detect_age_range(user_text)
        sex       = self._detect_sex(user_text)
        is_death  = any(k in user_text for k in ("사망", "죽"))
        is_surv   = any(k in user_text for k in ("생존", "살아남", "살았"))
        is_age_group = any(k in user_text for k in ("나이대", "연령대"))
        is_grade_group = any(k in user_text for k in ("등급별", "클래스별"))

        # ── 데이터 로드 (생존/사망 질문 포함 모든 경우) ───────────────────────
        train_set: DataFrame = await self.walter.get_train_set()
        test_set: DataFrame  = await self.walter.get_test_set()
        best_name, test_pred = await self._with_predictions(train_set, test_set)

        # ── 나이대별 브레이크다운 ─────────────────────────────────────────────
        if is_age_group:
            if is_surv or is_death:
                action = "사망자" if is_death else "생존자"
                lines = []
                for lbl, lo, hi in _AGE_GROUPS:
                    ar = (lo, hi)
                    tf = self._apply_filters(train_set, pclass, ar, sex)
                    vf = self._apply_filters(test_pred,  pclass, ar, sex)
                    total, survived, dead = self._stats(tf, vf)
                    if total == 0:
                        continue
                    count = dead if is_death else survived
                    lines.append(f"  • {lbl}: {count}명 ({count/total:.1%})")
                return f"나이대별 {action} 현황 (예측 포함 [{best_name}])\n" + "\n".join(lines)
            else:
                # 탑승객 수 + 생존/사망 브레이크다운
                age_all = pd.to_numeric(
                    pd.concat([train_set, test_set], ignore_index=True)["age"], errors="coerce"
                )
                unknown_cnt = int(age_all.isna().sum())
                lines = [f"  • 나이 미상: {unknown_cnt}명"]
                for lbl, lo, hi in _AGE_GROUPS:
                    ar = (lo, hi)
                    tf = self._apply_filters(train_set, pclass, ar, sex)
                    vf = self._apply_filters(test_pred,  pclass, ar, sex)
                    total, survived, dead = self._stats(tf, vf)
                    if total == 0:
                        continue
                    lines.append(
                        f"  • {lbl}: {total}명 | 생존 {survived}명({survived/total:.0%}) · 사망 {dead}명({dead/total:.0%})"
                    )
                return f"나이대별 탑승객 현황 (예측 포함 [{best_name}])\n" + "\n".join(lines)

        # ── 등급별 브레이크다운 ───────────────────────────────────────────────
        if is_grade_group:
            action = "사망자" if is_death else "생존자" if is_surv else "탑승객"
            lines = []
            for pc in ("1", "2", "3"):
                tf = self._apply_filters(train_set, pc, age_range, sex)
                vf = self._apply_filters(test_pred,  pc, age_range, sex)
                total, survived, dead = self._stats(tf, vf)
                if total == 0:
                    continue
                if is_death:
                    lines.append(f"  • {pc}등석: {dead}명 ({dead/total:.1%})")
                elif is_surv:
                    lines.append(f"  • {pc}등석: {survived}명 ({survived/total:.1%})")
                else:
                    lines.append(
                        f"  • {pc}등석: {total}명 | 생존 {survived}명({survived/total:.0%}) · 사망 {dead}명({dead/total:.0%})"
                    )
            return f"등급별 {action} 현황 (예측 포함 [{best_name}])\n" + "\n".join(lines)

        # ── 생존/사망 — 단일/조합 필터 ───────────────────────────────────────
        if is_surv or is_death:
            tf = self._apply_filters(train_set, pclass, age_range, sex)
            vf = self._apply_filters(test_pred,  pclass, age_range, sex)
            total, survived, dead = self._stats(tf, vf)

            label_parts: list[str] = []
            if pclass:    label_parts.append(f"{pclass}등석")
            if age_range: label_parts.append(self._age_range_label(age_range))
            if sex:       label_parts.append("여성" if sex == "female" else "남성")
            label = " ".join(label_parts) + " " if label_parts else ""

            if total == 0:
                return f"{label}승객 데이터가 없습니다."
            if is_death:
                d_known = len(tf) - int(pd.to_numeric(tf["survived"], errors="coerce").fillna(0).sum())
                d_pred  = len(vf) - int(vf["survived_pred"].sum())
                return (
                    f"{label}승객 {total}명 중 사망자는 약 {dead}명 ({dead/total:.1%})으로 추정됩니다.\n"
                    f"• 확인된 사망자: {d_known}명\n"
                    f"• [{best_name}] 예측 사망자: {d_pred}명"
                )
            s_known = int(pd.to_numeric(tf["survived"], errors="coerce").fillna(0).sum())
            s_pred  = int(vf["survived_pred"].sum())
            return (
                f"{label}승객 {total}명 중 생존자는 약 {survived}명 ({survived/total:.1%})으로 추정됩니다.\n"
                f"• 확인된 생존자: {s_known}명\n"
                f"• [{best_name}] 예측 생존자: {s_pred}명"
            )

        # ── 탑승 항구 ─────────────────────────────────────────────────────────
        embarked_map = {
            "사우샘프턴": "S", "Southampton": "S",
            "셰르부르":   "C", "Cherbourg":   "C",
            "퀸즈타운":   "Q", "Queenstown":  "Q",
        }
        for label, code in embarked_map.items():
            if label in user_text:
                tf = train_set[train_set["embarked"] == code]
                vf = test_pred[test_pred["embarked"] == code]
                total, survived, dead = self._stats(tf, vf)
                return (
                    f"{label} 출발 승객은 {total:,}명입니다.\n"
                    + self._surv_lines(total, survived, dead, best_name)
                )

        # ── 객실 등급 단독 ────────────────────────────────────────────────────
        if pclass:
            tf = self._apply_filters(train_set, pclass, age_range, sex)
            vf = self._apply_filters(test_pred,  pclass, age_range, sex)
            total, survived, dead = self._stats(tf, vf)
            sex_label = ("여성 " if sex == "female" else "남성 ") if sex else ""
            return (
                f"{pclass}등석 {sex_label}승객은 총 {total:,}명입니다.\n"
                + self._surv_lines(total, survived, dead, best_name)
            )

        # ── 성별 단독 ─────────────────────────────────────────────────────────
        if sex:
            tf = self._apply_filters(train_set, None, age_range, sex)
            vf = self._apply_filters(test_pred,  None, age_range, sex)
            total, survived, dead = self._stats(tf, vf)
            sex_label = "여성" if sex == "female" else "남성"
            return (
                f"{sex_label}은 총 {total:,}명입니다.\n"
                + self._surv_lines(total, survived, dead, best_name)
            )

        # ── 총 탑승객 수 ──────────────────────────────────────────────────────
        if any(k in user_text for k in ("탑승객", "승객", "탑승자", "몇명", "몇 명", "총")):
            total, survived, dead = self._stats(train_set, test_pred)
            return (
                f"타이타닉에는 총 {total:,}명의 승객이 탑승했습니다.\n"
                + self._surv_lines(total, survived, dead, best_name)
            )

        # ── 기본 안내 ─────────────────────────────────────────────────────────
        total = len(train_set) + len(test_set)
        return (
            f"타이타닉 승객 {total:,}명의 데이터를 보유하고 있습니다.\n"
            "탑승객 수, 생존자, 성별, 객실 등급(1·2·3등석), 나이대 등에 대해 물어보세요."
        )

    async def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        return await self.repository.introduce_myself(query)
