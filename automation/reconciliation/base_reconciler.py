from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Callable, Iterable, Mapping, Sequence

KeySelector = str | Callable[[Mapping[str, Any]], object]
RepairCallback = Callable[[dict[str, Any], dict[str, Any]], bool]


@dataclass(frozen=True, slots=True)
class FieldDifference:
    field: str
    local: Any
    remote: Any
    kind: str = "changed"


@dataclass(slots=True)
class ReconciliationReport:
    entity: str
    checked: int = 0
    matched: int = 0
    drifted: int = 0
    repaired: int = 0
    missing_local: int = 0
    missing_remote: int = 0
    duplicate_local: int = 0
    duplicate_remote: int = 0
    conflicts: int = 0
    errors: list[str] = field(default_factory=list)
    differences: dict[str, list[FieldDifference]] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors and self.conflicts == 0

    @property
    def coverage(self) -> float:
        total = self.matched + self.drifted + self.missing_local + self.missing_remote
        return round(self.matched / total, 6) if total else 1.0

    def as_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["ok"] = self.ok
        value["coverage"] = self.coverage
        return value


class BaseReconciler:
    """Deterministic bidirectional reconciler with deep comparison and repair hooks.

    The original ``reconcile(local, remote, key='id', repair=...)`` contract is
    preserved. New optional arguments allow field filtering, numeric tolerance,
    missing-side handlers and bounded difference capture without loading more
    than one remote index in memory.
    """

    def __init__(self, entity: str, *, maximum_differences: int = 500) -> None:
        self.entity = str(entity).strip() or "entity"
        self.maximum_differences = max(0, int(maximum_differences))
        self.last_report: ReconciliationReport | None = None

    def reconcile(
        self,
        local_items: Iterable[dict[str, Any]],
        remote_items: Iterable[dict[str, Any]],
        *,
        key: KeySelector = "id",
        repair: RepairCallback | None = None,
        create_local: Callable[[dict[str, Any]], bool] | None = None,
        create_remote: Callable[[dict[str, Any]], bool] | None = None,
        ignore_fields: Iterable[str] = (),
        compare_fields: Iterable[str] | None = None,
        numeric_tolerance: float = 0.0,
    ) -> ReconciliationReport:
        report = ReconciliationReport(self.entity)
        ignored = {str(item) for item in ignore_fields}
        selected = None if compare_fields is None else {str(item) for item in compare_fields}
        tolerance = max(0.0, float(numeric_tolerance))

        local_index, local_dupes = self._index(local_items, key)
        remote_index, remote_dupes = self._index(remote_items, key)
        report.duplicate_local = local_dupes
        report.duplicate_remote = remote_dupes
        report.conflicts += local_dupes + remote_dupes
        all_ids = sorted(set(local_index) | set(remote_index))

        for identifier in all_ids:
            local = local_index.get(identifier)
            remote = remote_index.get(identifier)
            report.checked += 1
            if local is None:
                report.missing_local += 1
                if create_local is not None:
                    self._invoke_missing(create_local, remote or {}, report, identifier)
                continue
            if remote is None:
                report.missing_remote += 1
                if create_remote is not None:
                    self._invoke_missing(create_remote, local, report, identifier)
                continue

            differences = self._differences(
                local,
                remote,
                ignored=ignored,
                selected=selected,
                numeric_tolerance=tolerance,
            )
            if not differences:
                report.matched += 1
                continue
            report.drifted += 1
            if self.maximum_differences and len(report.differences) < self.maximum_differences:
                report.differences[identifier] = differences
            if repair is not None:
                try:
                    if bool(repair(local, remote)):
                        report.repaired += 1
                except Exception as exc:  # repair failures must not abort the whole scan
                    report.errors.append(f"{identifier}: {type(exc).__name__}: {exc}"[:2000])

        report.metadata.update(
            {
                "key": key if isinstance(key, str) else getattr(key, "__name__", "callable"),
                "ignore_fields": sorted(ignored),
                "compare_fields": sorted(selected) if selected is not None else None,
                "numeric_tolerance": tolerance,
            }
        )
        self.last_report = report
        return report

    def _index(self, items: Iterable[dict[str, Any]], key: KeySelector) -> tuple[dict[str, dict[str, Any]], int]:
        result: dict[str, dict[str, Any]] = {}
        duplicates = 0
        for raw in items:
            item = dict(raw)
            identifier = self._identifier(item, key)
            if not identifier:
                identifier = f"__missing_key__:{len(result)}"
            if identifier in result:
                duplicates += 1
                continue
            result[identifier] = item
        return result, duplicates

    @staticmethod
    def _identifier(item: Mapping[str, Any], key: KeySelector) -> str:
        value = key(item) if callable(key) else item.get(key)
        return str(value).strip() if value is not None else ""

    def _differences(
        self,
        local: Mapping[str, Any],
        remote: Mapping[str, Any],
        *,
        ignored: set[str],
        selected: set[str] | None,
        numeric_tolerance: float,
    ) -> list[FieldDifference]:
        fields = set(local) | set(remote)
        fields -= ignored
        if selected is not None:
            fields &= selected
        differences: list[FieldDifference] = []
        for field_name in sorted(fields):
            left = local.get(field_name)
            right = remote.get(field_name)
            if self._equivalent(left, right, numeric_tolerance):
                continue
            kind = "missing_local" if field_name not in local else ("missing_remote" if field_name not in remote else "changed")
            differences.append(FieldDifference(field_name, left, right, kind))
        return differences

    @classmethod
    def _equivalent(cls, left: Any, right: Any, tolerance: float) -> bool:
        if left is right:
            return True
        if isinstance(left, Mapping) and isinstance(right, Mapping):
            keys = set(left) | set(right)
            return all(cls._equivalent(left.get(key), right.get(key), tolerance) for key in keys)
        if isinstance(left, Sequence) and isinstance(right, Sequence) and not isinstance(left, (str, bytes, bytearray)) and not isinstance(right, (str, bytes, bytearray)):
            return len(left) == len(right) and all(cls._equivalent(a, b, tolerance) for a, b in zip(left, right))
        if cls._numeric(left) is not None and cls._numeric(right) is not None:
            return abs(float(cls._numeric(left)) - float(cls._numeric(right))) <= tolerance
        if isinstance(left, str) and isinstance(right, str):
            return left.strip() == right.strip()
        return left == right

    @staticmethod
    def _numeric(value: Any) -> Decimal | None:
        if isinstance(value, bool) or value is None:
            return None
        if isinstance(value, (int, float, Decimal)):
            try:
                number = Decimal(str(value))
            except (InvalidOperation, ValueError):
                return None
            return number if number.is_finite() else None
        return None

    @staticmethod
    def _invoke_missing(callback: Callable[[dict[str, Any]], bool], value: dict[str, Any], report: ReconciliationReport, identifier: str) -> None:
        try:
            if callback(dict(value)):
                report.repaired += 1
        except Exception as exc:
            report.errors.append(f"{identifier}: {type(exc).__name__}: {exc}"[:2000])
