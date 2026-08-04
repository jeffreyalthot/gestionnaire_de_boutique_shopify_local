from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from time import monotonic
from typing import Any, Iterable, Mapping


@dataclass(frozen=True, slots=True)
class ReportEnvelope:
    name: str
    generated_at: str
    summary: dict[str, Any]
    rows: list[dict[str, Any]]
    duration_ms: float = 0.0
    row_count: int = 0
    fingerprint: str = ""
    warnings: tuple[str, ...] = ()
    parameters: dict[str, Any] | None = None
    schema: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class QueryReport:
    """Bounded SQLite report with stable fingerprints and safe exports."""

    name = "report"
    query = "SELECT 1 value"
    parameters: tuple[Any, ...] = ()
    maximum_rows = 10_000

    def __init__(self, db: Any, *, maximum_rows: int | None = None) -> None:
        self.db = db
        self.maximum_rows = max(1, min(int(maximum_rows or self.maximum_rows), 100_000))
        self.last_envelope: ReportEnvelope | None = None

    def build_query(self, **filters: Any) -> tuple[str, tuple[Any, ...]]:
        return self.query, self.parameters

    def normalize_row(self, row: Mapping[str, Any]) -> dict[str, Any]:
        return {str(key): value for key, value in row.items()}

    def summarize(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        return {"rows": len(rows)}

    def validate_rows(self, rows: list[dict[str, Any]]) -> tuple[str, ...]:
        warnings: list[str] = []
        if len(rows) >= self.maximum_rows:
            warnings.append("report_truncated")
        if rows and any(set(row) != set(rows[0]) for row in rows[1:]):
            warnings.append("heterogeneous_schema")
        return tuple(warnings)

    def generate_rows(self, **filters: Any) -> list[dict[str, Any]]:
        query, parameters = self.build_query(**filters)
        values = self.db.query(query, parameters)
        return [self.normalize_row(row) for row in list(values)[: self.maximum_rows]]

    def generate(self, **filters: Any) -> dict[str, Any]:
        started = monotonic()
        rows = self.generate_rows(**filters)
        summary = dict(self.summarize(rows))
        schema = tuple(sorted({key for row in rows for key in row}))
        canonical = json.dumps(
            {"name": self.name, "summary": summary, "rows": rows, "filters": filters},
            ensure_ascii=False,
            default=str,
            sort_keys=True,
            separators=(",", ":"),
        )
        envelope = ReportEnvelope(
            self.name,
            datetime.now(timezone.utc).isoformat(),
            summary,
            rows,
            round((monotonic() - started) * 1000, 3),
            len(rows),
            hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
            self.validate_rows(rows),
            dict(filters),
            schema,
        )
        self.last_envelope = envelope
        return envelope.as_dict()

    def export(self, path: Path, *, format: str = "json", **filters: Any) -> Path:
        envelope = self.generate(**filters)
        normalized = str(format).strip().lower()
        if normalized == "json":
            from reports.json_exporter import export_json

            return export_json(envelope, Path(path))
        if normalized == "csv":
            from reports.csv_exporter import export_csv

            return export_csv(list(envelope["rows"]), Path(path))
        raise ValueError(f"Format de rapport non supporté: {format}")


class TimeWindowReport(QueryReport):
    timestamp_field = "created_at"
    default_days = 1

    def build_query(self, **filters: Any) -> tuple[str, tuple[Any, ...]]:
        days = max(1, min(int(filters.get("days", self.default_days)), 3650))
        query = self.query.replace("{time_filter}", f"{self.timestamp_field}>=datetime('now', ?)")
        return query, (f"-{days} days", *self.parameters)


def aggregate(rows: Iterable[Mapping[str, Any]], field: str, *, digits: int = 2) -> float:
    total = 0.0
    for row in rows:
        try:
            total += float(row.get(field, 0) or 0)
        except (TypeError, ValueError):
            continue
    return round(total, digits)


def ratio(numerator: object, denominator: object, *, digits: int = 4) -> float:
    try:
        bottom = float(denominator or 0)
        top = float(numerator or 0)
    except (TypeError, ValueError):
        return 0.0
    return round(top / bottom, digits) if bottom else 0.0


def grouped_summary(rows: Iterable[Mapping[str, Any]], field: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for row in rows:
        key = str(row.get(field, "unknown") or "unknown")
        result[key] = result.get(key, 0) + 1
    return dict(sorted(result.items()))
