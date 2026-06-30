from __future__ import annotations

from enum import StrEnum


class SpamLabel(StrEnum):
    HAM = "ham"
    PHISHING = "phishing"
    ADVERTISEMENT = "advertisement"
    MALWARE = "malware"
    SCAM = "scam"


_DESCRIPTIONS: dict[SpamLabel, str] = {
    SpamLabel.HAM: "정상 메일",
    SpamLabel.PHISHING: "피싱",
    SpamLabel.ADVERTISEMENT: "광고",
    SpamLabel.MALWARE: "악성코드",
    SpamLabel.SCAM: "사기",
}


def description_of(label: SpamLabel) -> str:
    return _DESCRIPTIONS[label]
