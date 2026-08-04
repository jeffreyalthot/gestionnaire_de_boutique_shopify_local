from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class StockRecheckDecision:
    allowed: bool
    reason: str
    requested: int
    supplier_available: int | None
    remaining: int | None
    shortage: int
    safety_buffer: int

    def as_dict(self) -> dict[str, object]:
        return asdict(self)

    def __iter__(self):
        yield self.allowed
        yield self.reason


class StockRecheckService:
    def decide(
        self,
        requested: int,
        supplier_available: int | None,
        *,
        safety_buffer: int = 0,
        allow_partial: bool = False,
    ) -> StockRecheckDecision:
        quantity = int(requested)
        buffer = max(0, int(safety_buffer))
        if quantity <= 0:
            return StockRecheckDecision(False, "invalid_quantity", quantity, supplier_available, supplier_available, 0, buffer)
        if supplier_available is None:
            return StockRecheckDecision(False, "availability_unknown", quantity, None, None, quantity + buffer, buffer)
        available = max(0, int(supplier_available))
        required = quantity + buffer
        shortage = max(0, required - available)
        allowed = available >= required or (allow_partial and available > buffer)
        reason = "available" if available >= required else "partial_available" if allowed else "supplier_stock_shortage"
        return StockRecheckDecision(allowed, reason, quantity, available, max(0, available - quantity), shortage, buffer)

    def check(self, requested: int, supplier_available: int | None) -> tuple[bool, str]:
        decision = self.decide(requested, supplier_available)
        return decision.allowed, decision.reason
