from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class QueryCost:
    requested: int
    actual: int
    maximum_available: float
    currently_available: float
    restore_rate: float

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def query_cost(payload: dict[str, object]) -> QueryCost:
    extensions = payload.get("extensions", {})
    cost = extensions.get("cost", {}) if isinstance(extensions, dict) else {}
    throttle = cost.get("throttleStatus", {}) if isinstance(cost, dict) else {}
    return QueryCost(
        requested=int(cost.get("requestedQueryCost", 0) or 0),
        actual=int(cost.get("actualQueryCost", 0) or 0),
        maximum_available=float(throttle.get("maximumAvailable", 0) or 0),
        currently_available=float(throttle.get("currentlyAvailable", 0) or 0),
        restore_rate=float(throttle.get("restoreRate", 0) or 0),
    )


def requested_query_cost(payload: dict[str, object]) -> int:
    return query_cost(payload).requested


def estimate_wait_seconds(cost: QueryCost, next_requested: int) -> float:
    deficit = max(0.0, float(next_requested) - cost.currently_available)
    return deficit / cost.restore_rate if deficit and cost.restore_rate > 0 else 0.0
