from __future__ import annotations

from dataclasses import asdict, dataclass
from threading import RLock
from typing import Iterable


@dataclass(frozen=True, slots=True)
class ReservationResult:
    sku: str
    requested: int
    reserved: int
    total_reserved: int
    allowed: bool
    reason: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class InventoryReservation:
    def __init__(self) -> None:
        self._reserved: dict[str, int] = {}
        self._tokens: dict[str, tuple[str, int]] = {}
        self._lock = RLock()

    def reserve(self, sku: str, quantity: int, *, available: int | None = None,
                token: str = "") -> ReservationResult:
        sku = str(sku).strip(); quantity = int(quantity)
        if not sku or quantity <= 0:
            return ReservationResult(sku, quantity, 0, self.quantity(sku), False, "invalid_request")
        with self._lock:
            if token and token in self._tokens:
                prior_sku, prior_qty = self._tokens[token]
                return ReservationResult(prior_sku, prior_qty, prior_qty, self._reserved.get(prior_sku, 0), True, "idempotent_replay")
            current = self._reserved.get(sku, 0)
            if available is not None and current + quantity > max(0, int(available)):
                return ReservationResult(sku, quantity, 0, current, False, "insufficient_inventory")
            self._reserved[sku] = current + quantity
            if token: self._tokens[token] = (sku, quantity)
            return ReservationResult(sku, quantity, quantity, self._reserved[sku], True, "reserved")

    def reserve_many(self, lines: Iterable[dict[str, object]], availability: dict[str, int]) -> tuple[ReservationResult, ...]:
        results = []
        completed = []
        for line in lines:
            sku = str(line.get("sku", "")); quantity = int(line.get("quantity", 0) or 0)
            result = self.reserve(sku, quantity, available=availability.get(sku), token=str(line.get("token", "")))
            results.append(result)
            if not result.allowed:
                for reserved_sku, reserved_qty in completed:
                    self.release(reserved_sku, reserved_qty)
                break
            completed.append((sku, quantity))
        return tuple(results)

    def release(self, sku: str, quantity: int) -> int:
        with self._lock:
            self._reserved[sku] = max(0, self._reserved.get(sku, 0) - max(0, int(quantity)))
            return self._reserved[sku]

    def quantity(self, sku: str) -> int:
        with self._lock: return self._reserved.get(sku, 0)

    def snapshot(self) -> dict[str, int]:
        with self._lock: return dict(sorted(self._reserved.items()))
