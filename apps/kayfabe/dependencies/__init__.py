"""Kayfabe 의존성 조립소 (DIP 팩토리)."""

from __future__ import annotations

import importlib
from typing import Any

__all__ = [
    "get_ple_use_case",
    "get_pleinfo_use_case",
    "get_ranking_use_case",
    "get_records_use_case",
    "get_result_use_case",
    "get_title_history_use_case",
]

_LAZY_IMPORTS: dict[str, str] = {
    "get_ple_use_case": "kayfabe.dependencies.ple_provider",
    "get_pleinfo_use_case": "kayfabe.dependencies.pleinfo_provider",
    "get_ranking_use_case": "kayfabe.dependencies.ranking_provider",
    "get_records_use_case": "kayfabe.dependencies.records_provider",
    "get_result_use_case": "kayfabe.dependencies.result_provider",
    "get_title_history_use_case": "kayfabe.dependencies.title_history_provider",
}


def __getattr__(name: str) -> Any:
    module_path = _LAZY_IMPORTS.get(name)
    if module_path is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = importlib.import_module(module_path)
    return getattr(module, name)
