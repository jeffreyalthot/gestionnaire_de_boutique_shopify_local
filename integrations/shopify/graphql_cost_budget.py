from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from time import monotonic

@dataclass(frozen=True, slots=True)
class CostSnapshot:
    maximum_available: float
    currently_available: float
    restore_rate: float
    requested_cost: float
    actual_cost: float
    observed_at: float

class GraphqlCostBudget:
    """Modèle local conservateur du budget calculé de l'Admin GraphQL API."""
    def __init__(self, minimum_available: int = 100, maximum_requested: int = 1000) -> None:
        if minimum_available < 0 or maximum_requested <= 0:
            raise ValueError("Budget GraphQL invalide")
        self.minimum = float(minimum_available)
        self.maximum = float(maximum_requested)
        self._available = float(maximum_requested)
        self._restore_rate = 50.0
        self._requested = 0.0
        self._actual = 0.0
        self._observed_at = monotonic()
        self._lock = RLock()

    def _restored_available_locked(self, now: float | None = None) -> float:
        timestamp = monotonic() if now is None else now
        elapsed = max(0.0, timestamp - self._observed_at)
        return min(self.maximum, self._available + elapsed * self._restore_rate)

    @property
    def available(self) -> int:
        with self._lock:
            return int(self._restored_available_locked())

    def observe(self, extensions: dict[str, object] | None) -> CostSnapshot:
        with self._lock:
            now = monotonic()
            cost = (extensions or {}).get("cost", {})
            if not isinstance(cost, dict):
                return self.snapshot(now)
            throttle = cost.get("throttleStatus", {})
            if isinstance(throttle, dict):
                self.maximum = max(1.0, float(throttle.get("maximumAvailable", self.maximum)))
                self._available = max(0.0, float(throttle.get("currentlyAvailable", self._restored_available_locked(now))))
                self._restore_rate = max(0.01, float(throttle.get("restoreRate", self._restore_rate)))
            self._requested = max(0.0, float(cost.get("requestedQueryCost", 0.0)))
            self._actual = max(0.0, float(cost.get("actualQueryCost", self._requested)))
            self._observed_at = now
            return self.snapshot(now)

    def allows(self, estimated_cost: int | float) -> bool:
        estimate = max(0.0, float(estimated_cost))
        with self._lock:
            return estimate <= self.maximum and self._restored_available_locked() - estimate >= self.minimum

    def seconds_until_available(self, estimated_cost: int | float) -> float:
        estimate = max(0.0, float(estimated_cost))
        with self._lock:
            deficit = self.minimum + estimate - self._restored_available_locked()
            return 0.0 if deficit <= 0 else deficit / max(self._restore_rate, 0.01)

    def reserve(self, estimated_cost: int | float) -> bool:
        estimate = max(0.0, float(estimated_cost))
        with self._lock:
            now = monotonic()
            available = self._restored_available_locked(now)
            if estimate > self.maximum or available - estimate < self.minimum:
                return False
            self._available = available - estimate
            self._requested = estimate
            self._actual = 0.0
            self._observed_at = now
            return True

    def snapshot(self, now: float | None = None) -> CostSnapshot:
        with self._lock:
            timestamp = monotonic() if now is None else now
            return CostSnapshot(self.maximum, self._restored_available_locked(timestamp), self._restore_rate, self._requested, self._actual, timestamp)
