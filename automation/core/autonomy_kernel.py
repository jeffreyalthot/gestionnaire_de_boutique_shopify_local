from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from threading import RLock
from typing import Any, Iterable

from automation.core.autonomy_controller import AutonomyController
from automation.policies.rule_policy import RulePolicyDecision


@dataclass(frozen=True, slots=True)
class ActionProposal:
    name: str
    capability: str
    risk: str = "read_only"
    confidence: float = 1.0
    amount_cad: float = 0.0
    heavy: bool = False
    pending_tasks: int = 0
    entity_type: str = ""
    entity_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class KernelDecision:
    allowed: bool
    simulated: bool
    approval_required: bool
    reason: str
    proposal: ActionProposal
    policy_reasons: tuple[str, ...]
    decided_at: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class AutonomyKernel:
    """Single decision point for every externally visible automation action."""

    def __init__(self, *, capabilities: Any, governor: Any, lockdown: Any,
                 controller: AutonomyController, db: Any | None = None) -> None:
        self.capabilities = capabilities
        self.governor = governor
        self.lockdown = lockdown
        self.controller = controller
        self.db = db
        self._lock = RLock()
        self._counts = {"allowed": 0, "simulated": 0, "approval_required": 0, "rejected": 0}
        self._last: KernelDecision | None = None

    def decide(
        self,
        proposal: ActionProposal,
        *,
        approved: bool = False,
        policies: Iterable[RulePolicyDecision] = (),
    ) -> KernelDecision:
        policy_items = tuple(policies)
        policy_reasons = tuple(item.reason for item in policy_items if not item.allowed)
        lockdown = self.lockdown.snapshot()
        if lockdown.get("active"):
            decision = self._decision(False, False, False, "emergency_lockdown", proposal, policy_reasons)
        elif policy_reasons:
            approval_required = any(item.approval_required for item in policy_items if not item.allowed)
            decision = self._decision(False, False, approval_required, "policy_rejected", proposal, policy_reasons)
        else:
            capability_available = self.capabilities.allows(
                proposal.capability, live=not self.controller.dry_run
            )
            budget_allowed, budget_reason = self.governor.allow(
                heavy=proposal.heavy, pending_tasks=proposal.pending_tasks
            )
            if not budget_allowed:
                decision = self._decision(False, False, False, budget_reason, proposal, ())
            else:
                autonomy = self.controller.decide(
                    risk=proposal.risk,
                    confidence=proposal.confidence,
                    amount_cad=proposal.amount_cad,
                    approved=approved,
                    capability_available=capability_available,
                )
                decision = self._decision(
                    autonomy.allowed,
                    autonomy.simulated,
                    autonomy.approval_required,
                    autonomy.reason,
                    proposal,
                    (),
                )
        self._record(decision)
        return decision

    def _decision(self, allowed: bool, simulated: bool, approval_required: bool,
                  reason: str, proposal: ActionProposal,
                  policy_reasons: tuple[str, ...]) -> KernelDecision:
        return KernelDecision(
            allowed=allowed,
            simulated=simulated,
            approval_required=approval_required,
            reason=reason,
            proposal=proposal,
            policy_reasons=policy_reasons,
            decided_at=datetime.now(timezone.utc).isoformat(),
        )

    def _record(self, decision: KernelDecision) -> None:
        key = "simulated" if decision.allowed and decision.simulated else (
            "allowed" if decision.allowed else (
                "approval_required" if decision.approval_required else "rejected"
            )
        )
        with self._lock:
            self._counts[key] += 1
            self._last = decision
        if self.db is not None:
            self.db.insert_audit("automation.autonomy_decision", "autonomy-kernel", decision.as_dict())

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                "counts": dict(self._counts),
                "last": self._last.as_dict() if self._last else None,
                "dry_run": self.controller.dry_run,
                "minimum_confidence": self.controller.minimum_confidence,
                "financial_limit_cad": self.controller.financial_limit_cad,
            }
