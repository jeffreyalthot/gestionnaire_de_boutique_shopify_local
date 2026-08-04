from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class CapacityAssessment:
    supported: bool
    monthly_capacity: int
    committed: int
    requested: int
    usable_capacity: int
    remaining_after_order: int
    utilization_percent: float
    reason: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class SupplierCapacity:
    def can_support(self, *, monthly_capacity: int, committed: int, requested: int, buffer_percent: float = 10) -> bool:
        return self.assess(monthly_capacity=monthly_capacity, committed=committed, requested=requested, buffer_percent=buffer_percent).supported

    def assess(self, *, monthly_capacity: int, committed: int, requested: int, buffer_percent: float = 10) -> CapacityAssessment:
        capacity = max(0, int(monthly_capacity)); committed_value = max(0, int(committed)); request = int(requested)
        usable = max(0, int(capacity * (1 - max(0.0, min(100.0, buffer_percent)) / 100)) - committed_value)
        supported = request > 0 and usable >= request
        utilization = committed_value / capacity * 100 if capacity else 100.0
        reason = "supported" if supported else "invalid_request" if request <= 0 else "insufficient_capacity"
        return CapacityAssessment(supported, capacity, committed_value, request, usable, max(0, usable - max(0, request)), round(utilization, 2), reason)
