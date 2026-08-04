from __future__ import annotations

from collections import Counter, deque
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from math import isfinite
from threading import RLock
from typing import Any, Callable, Iterable, Mapping


@dataclass(frozen=True, slots=True)
class RulePolicyDecision:
    allowed: bool
    reason: str
    score: float = 1.0
    approval_required: bool = False
    detail: dict[str, Any] | None = None
    policy: str = "generic"
    evaluated_at: str = ""
    violations: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class RulePolicy:
    """Politique déterministe, composable et instrumentée."""

    name = "generic"

    def __init__(
        self,
        *,
        enabled: bool = True,
        minimum_score: float = 0.0,
        approval_on_failure: bool = True,
        maximum_violations: int = 0,
        validators: Iterable[Callable[[Mapping[str, Any]], str | None]] = (),
        history_size: int = 200,
    ) -> None:
        self.enabled = bool(enabled)
        self.minimum_score = self._score(minimum_score)
        self.approval_on_failure = bool(approval_on_failure)
        self.maximum_violations = max(0, int(maximum_violations))
        self.validators = tuple(validators)
        self._history: deque[RulePolicyDecision] = deque(maxlen=max(1, int(history_size)))
        self._reasons: Counter[str] = Counter()
        self._lock = RLock()

    @staticmethod
    def _score(value: Any) -> float:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return 0.0
        return max(0.0, min(1.0, number if isfinite(number) else 0.0))

    def _record(self, decision: RulePolicyDecision) -> RulePolicyDecision:
        with self._lock:
            self._history.append(decision)
            self._reasons[decision.reason] += 1
        return decision

    def evaluate(
        self,
        *,
        score: float = 1.0,
        violations: tuple[str, ...] = (),
        detail: dict[str, Any] | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> RulePolicyDecision:
        normalized_score = self._score(score)
        context_value = dict(context or {})
        collected = [str(item).strip() for item in violations if str(item).strip()]
        for validator in self.validators:
            violation = validator(context_value)
            if violation:
                collected.append(str(violation))
        unique_violations = tuple(sorted(set(collected)))
        evaluated_at = datetime.now(timezone.utc).isoformat()

        if not self.enabled:
            return self._record(RulePolicyDecision(False, "policy_disabled", normalized_score, True, detail, self.name, evaluated_at, unique_violations))
        if len(unique_violations) > self.maximum_violations:
            reason = "policy_violations:" + ",".join(unique_violations)
            return self._record(RulePolicyDecision(False, reason, normalized_score, self.approval_on_failure, detail, self.name, evaluated_at, unique_violations))
        if normalized_score < self.minimum_score:
            return self._record(RulePolicyDecision(False, "score_below_threshold", normalized_score, self.approval_on_failure, detail, self.name, evaluated_at, unique_violations))
        return self._record(RulePolicyDecision(True, "allowed", normalized_score, False, detail, self.name, evaluated_at, unique_violations))

    def evaluate_many(self, records: Iterable[Mapping[str, Any]]) -> tuple[RulePolicyDecision, ...]:
        return tuple(
            self.evaluate(
                score=record.get("score", 1.0),
                violations=tuple(record.get("violations", ())),
                detail=dict(record.get("detail", {})),
                context=record.get("context") if isinstance(record.get("context"), Mapping) else None,
            )
            for record in records
        )

    def statistics(self) -> dict[str, Any]:
        with self._lock:
            total = len(self._history)
            allowed = sum(decision.allowed for decision in self._history)
            return {
                "policy": self.name,
                "enabled": self.enabled,
                "minimum_score": self.minimum_score,
                "evaluated": total,
                "allowed": allowed,
                "blocked": total - allowed,
                "approval_required": sum(decision.approval_required for decision in self._history),
                "allow_rate": round(allowed / total, 6) if total else 0.0,
                "reasons": dict(self._reasons),
            }

    def recent(self, limit: int = 20) -> tuple[RulePolicyDecision, ...]:
        with self._lock:
            return tuple(list(self._history)[-max(1, int(limit)):])
