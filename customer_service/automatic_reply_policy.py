from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReplyDecision:
    automatic: bool
    reason: str


class AutomaticReplyPolicy:
    BLOCKED = {"chargeback", "fraud", "legal", "privacy", "threat", "medical_claim"}

    def evaluate(self, *, category: str, confidence: float, contains_sensitive_data: bool = False,
                 order_found: bool = True) -> ReplyDecision:
        if category in self.BLOCKED:
            return ReplyDecision(False, "sensitive_category")
        if contains_sensitive_data:
            return ReplyDecision(False, "sensitive_data")
        if not order_found and category != "general":
            return ReplyDecision(False, "missing_order_context")
        if confidence < 0.92:
            return ReplyDecision(False, "low_confidence")
        return ReplyDecision(True, "allowed")
