from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from numbers import Number
from typing import Any, Callable, Mapping

from rich.panel import Panel
from rich.table import Table
from rich.text import Text


@dataclass(frozen=True, slots=True)
class PanelField:
    label: str
    key: str
    formatter: str | Callable[[Any], str] = "text"
    default: Any = "-"


class StatePanel:
    """Fixed-height, bounded panel with nested fields and lightweight trends."""

    title = "Panel"
    fields: tuple[tuple[str, str] | PanelField, ...] = ()
    maximum_rows = 12

    def __init__(self, *, history_size: int = 30) -> None:
        self._history: deque[dict[str, Any]] = deque(maxlen=max(2, int(history_size)))
        self.last_rendered_at = ""

    def render(self, state: dict[str, Any] | Any) -> Panel:
        value = dict(state) if isinstance(state, Mapping) else {"value": state}
        self._history.append(value)
        self.last_rendered_at = datetime.now(timezone.utc).isoformat()
        table = Table(show_header=False, box=None, expand=True, padding=(0, 1))
        table.add_column("Metric", no_wrap=True)
        table.add_column("Value", justify="right", overflow="ellipsis")
        rows = self._rows(value)
        for label, rendered in rows[: self.maximum_rows]:
            table.add_row(label, rendered)
        footer = self._footer(value)
        return Panel(table, title=self.title, subtitle=footer, height=min(self.maximum_rows + 4, 20))

    def snapshot(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "history": len(self._history),
            "last_rendered_at": self.last_rendered_at,
            "latest": dict(self._history[-1]) if self._history else {},
        }

    def _rows(self, value: dict[str, Any]) -> list[tuple[str, str | Text]]:
        if self.fields:
            result: list[tuple[str, str | Text]] = []
            for field in self.fields:
                spec = field if isinstance(field, PanelField) else PanelField(field[0], field[1])
                raw = self._nested(value, spec.key, spec.default)
                result.append((spec.label, self._format(raw, spec.formatter, spec.key)))
            return result
        return [(str(key), self._format(value[key], "text", str(key))) for key in sorted(value)]

    def _footer(self, value: dict[str, Any]) -> str:
        status = str(value.get("status", value.get("state", "live"))).upper()
        return f"{status} | fixed rows | samples={len(self._history)}"

    @staticmethod
    def _nested(value: Mapping[str, Any], key: str, default: Any = "-") -> Any:
        current: Any = value
        for part in str(key).split("."):
            if not isinstance(current, Mapping) or part not in current:
                return default
            current = current[part]
        return current

    def _format(self, value: Any, formatter: str | Callable[[Any], str], key: str) -> str | Text:
        if callable(formatter):
            return formatter(value)
        kind = str(formatter)
        if kind == "money":
            try: return f"{float(value):,.2f} CAD"
            except (TypeError, ValueError): return "0.00 CAD"
        if kind == "percent":
            try: return f"{float(value):.1f}%"
            except (TypeError, ValueError): return "0.0%"
        if kind == "ratio":
            try: return f"{float(value):.3f}"
            except (TypeError, ValueError): return "0.000"
        if kind == "integer":
            try: return f"{int(value):,}"
            except (TypeError, ValueError): return "0"
        if kind == "bytes":
            try:
                number = float(value)
                for unit in ("B", "KiB", "MiB", "GiB"):
                    if abs(number) < 1024 or unit == "GiB": return f"{number:.1f} {unit}"
                    number /= 1024
            except (TypeError, ValueError): return "0 B"
        if kind == "bool":
            return Text("YES" if bool(value) else "NO", style="green" if bool(value) else "red")
        if kind == "status":
            normalized = str(value or "unknown").lower()
            style = "green" if normalized in {"ok", "ready", "healthy", "completed", "active"} else ("yellow" if normalized in {"pending", "degraded", "warning", "dry"} else "red")
            return Text(normalized.upper(), style=style)
        if isinstance(value, Number):
            trend = self._trend(key, float(value))
            suffix = " ↑" if trend > 0 else (" ↓" if trend < 0 else "")
            return f"{value}{suffix}"
        if isinstance(value, (list, tuple, set)):
            return ", ".join(map(str, list(value)[:5])) + ("…" if len(value) > 5 else "")
        if isinstance(value, Mapping):
            return ", ".join(f"{k}={v}" for k, v in list(value.items())[:5])
        return str(value)

    def _trend(self, key: str, current: float) -> int:
        if len(self._history) < 2:
            return 0
        previous = self._nested(self._history[-2], key, current)
        try: old = float(previous)
        except (TypeError, ValueError): return 0
        return 1 if current > old else (-1 if current < old else 0)
