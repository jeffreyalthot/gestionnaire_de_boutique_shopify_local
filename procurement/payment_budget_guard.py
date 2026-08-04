from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class PaymentBudgetDecision:
    allowed: bool
    reason: str
    requested_cad: Decimal
    remaining_daily_budget_cad: Decimal
    cash_after_cad: Decimal
    approval_required: bool

    def as_dict(self) -> dict[str, object]:
        return {key: str(value) if isinstance(value, Decimal) else value for key, value in asdict(self).items()}


class PaymentBudgetGuard:
    def evaluate(self, *, requested_cad: float, spent_today_cad: float, daily_budget_cad: float,
                 reserve_cad: float, cash_cad: float) -> tuple[bool, str]:
        decision = self.decide(requested_cad=requested_cad, spent_today_cad=spent_today_cad,
                               daily_budget_cad=daily_budget_cad, reserve_cad=reserve_cad,
                               cash_cad=cash_cad)
        return decision.allowed, decision.reason

    def decide(self, *, requested_cad: float, spent_today_cad: float, daily_budget_cad: float,
               reserve_cad: float, cash_cad: float, approval_threshold_cad: float = 1000) -> PaymentBudgetDecision:
        requested = Decimal(str(requested_cad)); spent = Decimal(str(spent_today_cad))
        daily = Decimal(str(daily_budget_cad)); reserve = Decimal(str(reserve_cad)); cash = Decimal(str(cash_cad))
        remaining = max(Decimal("0"), daily - spent); cash_after = cash - requested
        if requested <= 0: return PaymentBudgetDecision(False, "invalid_amount", requested, remaining, cash_after, False)
        if requested > remaining: return PaymentBudgetDecision(False, "daily_budget_exceeded", requested, remaining, cash_after, True)
        if cash_after < reserve: return PaymentBudgetDecision(False, "cash_reserve_breached", requested, remaining, cash_after, True)
        return PaymentBudgetDecision(True, "allowed", requested, remaining - requested, cash_after, requested >= Decimal(str(approval_threshold_cad)))
