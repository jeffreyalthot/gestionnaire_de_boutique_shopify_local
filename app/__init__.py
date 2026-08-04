"""Application package with lazy exports to avoid dashboard/bootstrap cycles."""

from __future__ import annotations

from typing import Any

__all__ = ["Application", "bootstrap"]


def __getattr__(name: str) -> Any:
    if name == "Application":
        from app.application import Application

        return Application
    if name == "bootstrap":
        from app.bootstrap import bootstrap

        return bootstrap
    raise AttributeError(name)
