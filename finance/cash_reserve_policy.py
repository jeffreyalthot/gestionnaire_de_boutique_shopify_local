from __future__ import annotations


class CashReservePolicy:
    def calculate(self, *, trailing_refunds_cad: float, trailing_chargebacks_cad: float,
                  pending_supplier_payments_cad: float, fixed_operating_cost_cad: float,
                  safety_multiplier: float = 1.25) -> dict[str, float]:
        components = {
            "refunds": max(0.0, trailing_refunds_cad),
            "chargebacks": max(0.0, trailing_chargebacks_cad),
            "supplier_payments": max(0.0, pending_supplier_payments_cad),
            "operations": max(0.0, fixed_operating_cost_cad),
        }
        required = sum(components.values()) * max(1.0, safety_multiplier)
        return {**{key: round(value, 2) for key, value in components.items()}, "required_reserve_cad": round(required, 2)}
