from __future__ import annotations


class EndOfLifePolicy:
    def evaluate(self, *, supplier_active: bool, stock: int, sales_90d: int,
                 margin_percent: float, compliance_ok: bool) -> dict[str, object]:
        if not compliance_ok:
            return {"action": "quarantine", "reason": "compliance_failure"}
        if not supplier_active and stock <= 0:
            return {"action": "archive", "reason": "supplier_unavailable"}
        if sales_90d <= 0 and stock <= 0:
            return {"action": "archive", "reason": "inactive"}
        if margin_percent < 20:
            return {"action": "review", "reason": "unprofitable"}
        return {"action": "keep", "reason": "healthy"}
