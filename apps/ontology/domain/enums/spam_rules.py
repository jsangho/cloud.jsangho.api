from __future__ import annotations

from dataclasses import dataclass

from ontology.domain.enums.spam_classes import SpamLabel


@dataclass(frozen=True)
class SpamRule:
    keyword: str
    label: SpamLabel
    weight: float = 1.0


RULES: tuple[SpamRule, ...] = (
    SpamRule("계정", SpamLabel.PHISHING),
    SpamRule("비밀번호", SpamLabel.PHISHING),
    SpamRule("긴급", SpamLabel.PHISHING),
    SpamRule("클릭하세요", SpamLabel.PHISHING),
    SpamRule("로그인 확인", SpamLabel.PHISHING),
    SpamRule("무료", SpamLabel.ADVERTISEMENT, weight=0.8),
    SpamRule("할인", SpamLabel.ADVERTISEMENT, weight=0.8),
    SpamRule("특가", SpamLabel.ADVERTISEMENT),
    SpamRule("이벤트 당첨", SpamLabel.ADVERTISEMENT),
    SpamRule("당첨", SpamLabel.SCAM),
    SpamRule("송금", SpamLabel.SCAM),
    SpamRule("환불", SpamLabel.SCAM, weight=0.9),
    SpamRule("다운로드", SpamLabel.MALWARE, weight=0.7),
    SpamRule("첨부파일 실행", SpamLabel.MALWARE),
    SpamRule("업데이트 필요", SpamLabel.MALWARE, weight=0.9),
)
