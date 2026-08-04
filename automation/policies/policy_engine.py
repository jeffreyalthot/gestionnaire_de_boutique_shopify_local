from __future__ import annotations

import hashlib
import json
from collections import Counter, deque
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from threading import RLock
from typing import Any, Iterable, Mapping


@dataclass(frozen=True, slots=True)
class ActionPolicy:
    action: str
    risk: str = "read_only"
    max_amount_cad: float = 0.0
    requires_approval: bool = False
    reversible: bool = True
    required_capabilities: tuple[str, ...] = ()
    blocked_modes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    allowed: bool
    simulated: bool
    approval_required: bool
    reason: str
    decision_id: str = ""
    evaluated_at: str = ""
    amount_cad: float = 0.0
    warnings: tuple[str, ...] = ()


class PolicyEngine:
    def __init__(
        self,
        *,
        dry_run: bool,
        financial_limit_cad: float = 1000.0,
        capabilities: Iterable[str] = (),
        mode: str | None = None,
        history_size: int = 500,
    ) -> None:
        self.dry_run = bool(dry_run)
        self.financial_limit_cad = max(0.0, float(financial_limit_cad))
        self.capabilities = frozenset(str(item) for item in capabilities)
        self.mode = str(mode or ("dry_run" if dry_run else "live"))
        self._history: deque[PolicyDecision] = deque(maxlen=max(1, int(history_size)))
        self._reasons: Counter[str] = Counter()
        self._lock = RLock()

    @staticmethod
    def _amount(value: Any) -> Decimal:
        try:
            amount = Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError) as exc:
            raise ValueError("invalid_amount") from exc
        if not amount.is_finite():
            raise ValueError("invalid_amount")
        return amount

    def _decision(
        self,
        policy: ActionPolicy,
        *,
        allowed: bool,
        simulated: bool,
        approval_required: bool,
        reason: str,
        amount: Decimal,
        warnings: tuple[str, ...] = (),
    ) -> PolicyDecision:
        evaluated_at = datetime.now(timezone.utc).isoformat()
        material = json.dumps(
            {
                "policy": asdict(policy),
                "allowed": allowed,
                "simulated": simulated,
                "reason": reason,
                "amount": str(amount),
                "mode": self.mode,
                "evaluated_at": evaluated_at,
            },
            sort_keys=True,
            default=str,
            separators=(",", ":"),
        )
        decision = PolicyDecision(
            allowed,
            simulated,
            approval_required,
            reason,
            hashlib.sha256(material.encode("utf-8")).hexdigest()[:24],
            evaluated_at,
            float(amount),
            warnings,
        )
        with self._lock:
            self._history.append(decision)
            self._reasons[reason] += 1
        return decision

    def evaluate(
        self,
        policy: ActionPolicy,
        *,
        amount_cad: float = 0.0,
        approved: bool = False,
        context: Mapping[str, Any] | None = None,
    ) -> PolicyDecision:
        try:
            amount = self._amount(amount_cad)
        except ValueError:
            amount = Decimal("0")
            return self._decision(policy, allowed=False, simulated=self.dry_run, approval_required=True, reason="invalid_amount", amount=amount)

        financial = policy.risk == "financial"
        irreversible = policy.risk == "irreversible" or not policy.reversible
        approval_required = policy.requires_approval or financial or irreversible
        warnings: list[str] = []
        action = str(policy.action).strip()
        if not action or len(action) > 160:
            return self._decision(policy, allowed=False, simulated=self.dry_run, approval_required=True, reason="invalid_action", amount=amount)
        if amount < 0:
            return self._decision(policy, allowed=False, simulated=self.dry_run, approval_required=approval_required, reason="negative_amount", amount=amount)
        if self.mode in set(policy.blocked_modes):
            return self._decision(policy, allowed=False, simulated=self.dry_run, approval_required=approval_required, reason="mode_blocked", amount=amount)
        missing_capabilities = tuple(sorted(set(policy.required_capabilities) - self.capabilities))
        if missing_capabilities:
            return self._decision(policy, allowed=False, simulated=self.dry_run, approval_required=approval_required, reason="missing_capability", amount=amount, warnings=missing_capabilities)
        limit = Decimal(str(policy.max_amount_cad or self.financial_limit_cad))
        if financial and amount > limit:
            return self._decision(policy, allowed=False, simulated=self.dry_run, approval_required=True, reason="financial_limit_exceeded", amount=amount)
        if context and context.get("emergency_stop"):
            return self._decision(policy, allowed=False, simulated=self.dry_run, approval_required=True, reason="emergency_stop", amount=amount)
        if context and context.get("stale_data"):
            warnings.append("stale_data")
            if financial or irreversible:
                return self._decision(policy, allowed=False, simulated=self.dry_run, approval_required=True, reason="fresh_data_required", amount=amount, warnings=tuple(warnings))
        if self.dry_run:
            return self._decision(policy, allowed=True, simulated=True, approval_required=approval_required, reason="dry_run_simulation", amount=amount, warnings=tuple(warnings))
        if approval_required and not approved:
            return self._decision(policy, allowed=False, simulated=False, approval_required=True, reason="explicit_approval_required", amount=amount, warnings=tuple(warnings))
        return self._decision(policy, allowed=True, simulated=False, approval_required=approval_required, reason="allowed", amount=amount, warnings=tuple(warnings))

    def evaluate_many(self, requests: Iterable[tuple[ActionPolicy, float, bool]]) -> tuple[PolicyDecision, ...]:
        return tuple(self.evaluate(policy, amount_cad=amount, approved=approved) for policy, amount, approved in requests)

    def explain(self, decision: PolicyDecision) -> dict[str, Any]:
        return asdict(decision)

    def statistics(self) -> dict[str, Any]:
        with self._lock:
            total = len(self._history)
            allowed = sum(item.allowed for item in self._history)
            return {
                "mode": self.mode,
                "dry_run": self.dry_run,
                "evaluated": total,
                "allowed": allowed,
                "blocked": total - allowed,
                "simulated": sum(item.simulated for item in self._history),
                "approval_required": sum(item.approval_required for item in self._history),
                "reasons": dict(self._reasons),
            }
