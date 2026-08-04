from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from collections import deque
from typing import Any, Iterable, Mapping


@dataclass(frozen=True, slots=True)
class AgentDecision:
    agent: str
    decision: str
    confidence: float
    score: float
    reasons: tuple[str, ...]
    approval_required: bool = False
    blocked: bool = False
    decision_id: str = ""
    recommended_actions: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class PolicyAwareAgent:
    """Deterministic, explainable and replayable business agent."""

    description = "Agent métier"
    positive_signals: tuple[str, ...] = ()
    negative_signals: tuple[str, ...] = ()
    hard_block_signals: tuple[str, ...] = ()
    approval_signals: tuple[str, ...] = ("financial_action", "irreversible_action")
    signal_weights: Mapping[str, float] = {}
    approve_threshold = 0.82
    reject_threshold = 0.35
    history_size = 200

    def __init__(self) -> None:
        self._history: deque[dict[str, Any]] = deque(maxlen=max(1, int(self.history_size)))
        self.total_decisions = 0
        self.approved = 0
        self.reviewed = 0
        self.rejected = 0

    @staticmethod
    def _ratio(numerator: Any, denominator: Any, default: float = 0.0) -> float:
        try:
            bottom = float(denominator)
            return float(numerator) / bottom if bottom else default
        except (TypeError, ValueError, ZeroDivisionError):
            return default

    def prepare_context(self, context: dict[str, Any]) -> dict[str, Any]:
        """Hook for domain agents to derive normalized signals from raw records."""
        return dict(context)

    def validate_context(self, context: dict[str, Any]) -> tuple[str, ...]:
        warnings: list[str] = []
        for name in (*self.positive_signals, *self.negative_signals):
            if name in context and not 0.0 <= self._bounded(context.get(name)) <= 1.0:
                warnings.append(f"signal_out_of_range:{name}")
        return tuple(warnings)

    @staticmethod
    def _bounded(value: Any, default: float = 0.0) -> float:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return default
        if number != number or number in (float("inf"), float("-inf")):
            return default
        return max(0.0, min(1.0, number))

    @staticmethod
    def _truthy(context: dict[str, Any], names: Iterable[str]) -> tuple[str, ...]:
        return tuple(name for name in names if bool(context.get(name)))

    def score(self, context: dict[str, Any]) -> tuple[float, tuple[str, ...]]:
        explicit = context.get("score")
        if explicit is not None:
            value = self._bounded(explicit, 0.5)
            return value, ("explicit_score",)
        numerator = self._bounded(context.get("confidence"), 0.75)
        denominator = 1.0
        reasons: list[str] = []
        for name in self.positive_signals:
            weight = max(0.01, float(self.signal_weights.get(name, 1.0)))
            value = self._bounded(context.get(name), 0.5)
            numerator += value * weight
            denominator += weight
            if value >= .7:
                reasons.append(f"positive:{name}")
        positive_score = numerator / denominator
        penalty_total = 0.0
        penalty_weight = 0.0
        for name in self.negative_signals:
            weight = max(0.01, float(self.signal_weights.get(name, 1.0)))
            value = self._bounded(context.get(name), 0.0)
            penalty_total += value * weight
            penalty_weight += weight
            if value >= .5:
                reasons.append(f"negative:{name}")
        penalty = (penalty_total / penalty_weight) * .65 if penalty_weight else 0.0
        value = max(0.0, min(1.0, positive_score - penalty))
        return value, tuple(reasons) or ("baseline_confidence",)

    def decide(self, context: dict[str, Any]) -> dict[str, Any]:
        context = self.prepare_context(dict(context))
        warnings = self.validate_context(context)
        hard_blocks = self._truthy(context, self.hard_block_signals)
        approval_reasons = self._truthy(context, self.approval_signals)
        score, reasons = self.score(context)
        if hard_blocks:
            decision_name, confidence, blocked = "reject", min(score, .2), True
            reasons = tuple(f"blocked:{name}" for name in hard_blocks)
        elif score < self.reject_threshold:
            decision_name, confidence, blocked = "reject", 1.0 - score, False
        elif approval_reasons or score < self.approve_threshold:
            decision_name, confidence, blocked = "review", max(score, 1.0 - score), False
            reasons = reasons + tuple(f"approval:{name}" for name in approval_reasons)
        else:
            decision_name, confidence, blocked = "approve", score, False
        material = json.dumps({"agent": self.__class__.__name__, "context": context, "decision": decision_name}, sort_keys=True, default=str)
        decision_id = hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]
        recommendations = self.recommend(context, decision_name, reasons)
        decision = AgentDecision(
            self.__class__.__name__, decision_name, round(confidence, 6), round(score, 6),
            reasons, bool(approval_reasons), blocked, decision_id, recommendations,
        )
        payload = decision.to_dict()
        payload["description"] = self.description
        payload["warnings"] = warnings
        self.total_decisions += 1
        if decision_name == "approve": self.approved += 1
        elif decision_name == "review": self.reviewed += 1
        else: self.rejected += 1
        self._history.append(dict(payload))
        return payload

    def history(self, limit: int = 20) -> tuple[dict[str, Any], ...]:
        return tuple(list(self._history)[-max(1, min(int(limit), self.history_size)):])

    def statistics(self) -> dict[str, Any]:
        return {
            "agent": self.__class__.__name__, "total": self.total_decisions,
            "approved": self.approved, "reviewed": self.reviewed, "rejected": self.rejected,
            "approval_rate": round(self.approved / self.total_decisions, 6) if self.total_decisions else 0.0,
            "history_size": len(self._history),
        }

    def recommend(self, context: dict[str, Any], decision: str, reasons: tuple[str, ...]) -> tuple[str, ...]:
        if decision == "approve":
            return ("continue_with_audit",)
        actions = []
        for reason in reasons:
            if reason.startswith("blocked:"):
                actions.append("stop_and_escalate")
            elif reason.startswith("negative:"):
                actions.append(f"reduce_{reason.split(':', 1)[1]}")
            elif reason.startswith("approval:"):
                actions.append("request_human_approval")
        return tuple(dict.fromkeys(actions or ("manual_review",)))

    def decide_many(self, contexts: Iterable[dict[str, Any]]) -> tuple[dict[str, Any], ...]:
        return tuple(self.decide(context) for context in contexts)
