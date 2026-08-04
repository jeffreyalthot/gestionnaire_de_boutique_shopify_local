from __future__ import annotations

from typing import Any


def money(value: object) -> str:
    try:
        return f"{float(value):,.2f} CAD"
    except (TypeError, ValueError):
        return "0.00 CAD"


def section(title: str, width: int) -> list[str]:
    return ["-" * width, title]


def value(row: dict[str, Any] | None, key: str, default: object = 0) -> object:
    return (row or {}).get(key, default)
