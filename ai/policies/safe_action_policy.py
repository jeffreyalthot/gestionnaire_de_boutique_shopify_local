from __future__ import annotations
from dataclasses import dataclass

_FORBIDDEN = frozenset({
    "store_card_number", "store_cvv", "disable_audit", "bypass_payment_confirmation",
    "disable_hmac", "log_access_token", "export_customer_pii_unencrypted", "ignore_product_restriction",
})

@dataclass(frozen=True, slots=True)
class SafeActionDecision:
    safe: bool
    action: str
    reason: str

class SafeActionPolicy:
    def __init__(self, forbidden: set[str] | None = None) -> None:
        self.forbidden = frozenset(_FORBIDDEN | {self.normalize(item) for item in (forbidden or set())})
    @staticmethod
    def normalize(action: str) -> str:
        return action.strip().lower().replace("-", "_").replace(" ", "_")
    def evaluate(self, action: str) -> SafeActionDecision:
        normalized = self.normalize(action)
        if not normalized:
            return SafeActionDecision(False, normalized, "Action vide.")
        if normalized in self.forbidden:
            return SafeActionDecision(False, normalized, "Action interdite par la politique de sécurité.")
        if normalized.startswith(("bypass_", "disable_security_", "store_raw_payment_")):
            return SafeActionDecision(False, normalized, "Famille d'action interdite.")
        return SafeActionDecision(True, normalized, "Action admissible.")

def safe_action(action: str) -> bool:
    return SafeActionPolicy().evaluate(action).safe
