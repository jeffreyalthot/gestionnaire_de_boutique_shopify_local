from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CustomerContext:
    customer_id: str
    lifetime_orders: int = 0
    lifetime_value_cad: float = 0.0
    refunds: int = 0
    chargebacks: int = 0
    account_age_days: int = 0
    country_code: str = ""

    @property
    def established(self) -> bool:
        return self.account_age_days >= 30 and self.lifetime_orders >= 2 and self.chargebacks == 0

    @property
    def refund_rate(self) -> float:
        return self.refunds / max(1, self.lifetime_orders)
