from __future__ import annotations

from dataclasses import dataclass

TITLE_STYLE = "bold cyan"
OK_STYLE = "green"
WARNING_STYLE = "yellow"
ERROR_STYLE = "bold red"
MUTED_STYLE = "dim"
INFO_STYLE = "cyan"


@dataclass(frozen=True, slots=True)
class StatusTheme:
    label: str
    style: str
    ascii_marker: str


_STATUS = {
    "ok": StatusTheme("OK", OK_STYLE, "+"),
    "healthy": StatusTheme("OK", OK_STYLE, "+"),
    "running": StatusTheme("ACTIF", OK_STYLE, ">"),
    "pending": StatusTheme("ATTENTE", WARNING_STYLE, "~"),
    "warning": StatusTheme("ALERTE", WARNING_STYLE, "!"),
    "error": StatusTheme("ERREUR", ERROR_STYLE, "X"),
    "failed": StatusTheme("ECHEC", ERROR_STYLE, "X"),
    "disabled": StatusTheme("INACTIF", MUTED_STYLE, "-"),
    "unknown": StatusTheme("INCONNU", MUTED_STYLE, "?"),
}


def status_theme(status: str) -> StatusTheme:
    return _STATUS.get(str(status).strip().lower(), _STATUS["unknown"])


def status_marker(status: str) -> str:
    item = status_theme(status)
    return f"[{item.ascii_marker}] {item.label}"
