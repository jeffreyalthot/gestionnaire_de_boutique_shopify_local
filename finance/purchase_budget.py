from __future__ import annotations


class PurchaseBudget:
    def authorize(self, *, available_cash_cad: float, protected_reserve_cad: float,
                  open_payables_cad: float, requested_cad: float) -> dict[str, object]:
        capacity = max(0.0, available_cash_cad - protected_reserve_cad - open_payables_cad)
        requested = max(0.0, requested_cad)
        return {"authorized": requested <= capacity, "capacity_cad": round(capacity, 2),
                "requested_cad": round(requested, 2), "remaining_cad": round(max(0.0, capacity - requested), 2)}
