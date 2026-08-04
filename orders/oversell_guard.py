from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AllocationDecision:
    allowed: bool
    allocatable: int
    reason: str


def allocate(available: int, requested: int, safety_stock: int = 0, already_reserved: int = 0) -> AllocationDecision:
    free = max(0, available - safety_stock - already_reserved)
    if requested <= 0:
        return AllocationDecision(False, 0, "invalid_quantity")
    if free < requested:
        return AllocationDecision(False, free, "insufficient_stock")
    return AllocationDecision(True, requested, "allocated")
