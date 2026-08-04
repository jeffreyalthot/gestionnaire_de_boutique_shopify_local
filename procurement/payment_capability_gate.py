from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class PaymentCapabilityDecision:
    allowed: bool
    reason: str
    simulated: bool
    approval_required: bool
    provider_ready: bool
    amount_cad: float
    within_limit: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)

    def __iter__(self):
        yield self.allowed
        yield self.reason


class PaymentCapabilityGate:
    def __init__(self, maximum_amount_cad: float = 5_000.0) -> None:
        self.maximum_amount_cad = max(0.0, float(maximum_amount_cad))

    def decide(
        self,
        *,
        provider_ready: bool,
        approved: bool,
        dry_run: bool,
        amount_cad: float = 0.0,
        currency: str = "CAD",
        capability_enabled: bool = True,
    ) -> PaymentCapabilityDecision:
        amount = round(max(0.0, float(amount_cad)), 2)
        normalized_currency = str(currency or "CAD").upper()
        within_limit = amount <= self.maximum_amount_cad
        if dry_run:
            return PaymentCapabilityDecision(True, "simulated", True, False, provider_ready, amount, within_limit)
        if normalized_currency != "CAD":
            return PaymentCapabilityDecision(False, "unsupported_currency", False, False, provider_ready, amount, within_limit)
        if not capability_enabled:
            return PaymentCapabilityDecision(False, "capability_disabled", False, False, provider_ready, amount, within_limit)
        if not provider_ready:
            return PaymentCapabilityDecision(False, "provider_not_ready", False, False, False, amount, within_limit)
        if not within_limit:
            return PaymentCapabilityDecision(False, "amount_limit_exceeded", False, True, True, amount, False)
        if not approved:
            return PaymentCapabilityDecision(False, "approval_required", False, True, True, amount, True)
        return PaymentCapabilityDecision(True, "allowed", False, False, True, amount, True)

    def evaluate(self, *, provider_ready: bool, approved: bool, dry_run: bool) -> tuple[bool, str]:
        decision = self.decide(provider_ready=provider_ready, approved=approved, dry_run=dry_run)
        return decision.allowed, decision.reason
