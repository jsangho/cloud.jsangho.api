from __future__ import annotations

from typing import Iterable


def _format_preview(
    *,
    title: str,
    data: dict[str, object],
    fields: Iterable[tuple[str, str]],
) -> str:
    fields_list = list(fields)
    label_width = max((len(label) for _, label in fields_list), default=0)
    lines = [title]
    for field, label in fields_list:
        value = data.get(field, "")
        lines.append(f"  {label:<{label_width}} : {value}")
    return "\n".join(lines)


SIGNUP_PREVIEW_FIELDS: tuple[tuple[str, str], ...] = (
    ("login_id", "userId"),
    ("nickname", "nickname"),
    ("email", "email"),
    ("role", "role"),
)

LOGIN_PREVIEW_FIELDS: tuple[tuple[str, str], ...] = (("login_id", "userId"),)

PROFILE_REQUEST_PREVIEW_FIELDS: tuple[tuple[str, str], ...] = (("user_id", "userId"),)

PROFILE_RESPONSE_PREVIEW_FIELDS: tuple[tuple[str, str], ...] = (
    ("id", "userId"),
    ("login_id", "loginId"),
    ("nickname", "nickname"),
    ("email", "email"),
    ("role", "role"),
)


def format_preview_signup(index: int, *, login_id: str, nickname: str, email: str, role: str) -> str:
    return _format_preview(
        title=f"── row {index} " + "─" * 40,
        data={
            "login_id": login_id,
            "nickname": nickname,
            "email": email,
            "role": role,
        },
        fields=SIGNUP_PREVIEW_FIELDS,
    )


def format_preview_login(index: int, *, login_id: str) -> str:
    return _format_preview(
        title=f"── row {index} " + "─" * 40,
        data={"login_id": login_id},
        fields=LOGIN_PREVIEW_FIELDS,
    )


def format_preview_profile_request(index: int, *, user_id: int) -> str:
    return _format_preview(
        title=f"── row {index} " + "─" * 40,
        data={"user_id": user_id},
        fields=PROFILE_REQUEST_PREVIEW_FIELDS,
    )


def format_preview_profile_response(index: int, *, user: dict[str, object]) -> str:
    return _format_preview(
        title=f"── row {index} " + "─" * 40,
        data=user,
        fields=PROFILE_RESPONSE_PREVIEW_FIELDS,
    )

