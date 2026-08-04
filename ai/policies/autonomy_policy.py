from __future__ import annotations

from dataclasses import asdict, dataclass

from ai.policies.confidence_policy import evaluate_confidence
from ai.policies.human_approval_policy import approval_requirement
from ai.policies.safe_action_policy import SafeActionPolicy


@dataclass(frozen=True, slots=True)
class AutonomyPolicyDecision:
    allowed: bool
    approval_required: bool
    action: str
    reason: str
    confidence: float
    required_confidence: float

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def evaluate_autonomy(action: str, confidence: float, minimum: float, *, amount_cad: float = 0.0,
                      financial: bool = False, irreversible: bool = False, risk_score: float = 0.0,
                      approved: bool = False) -> AutonomyPolicyDecision:
    safe = SafeActionPolicy().evaluate(action)
    if not safe.safe:
        return AutonomyPolicyDecision(False, False, safe.action, safe.reason, confidence, minimum)
    requirement = approval_requirement(safe.action, amount_cad, 0.0, irreversible=irreversible, financial=financial)
    conf = evaluate_confidence(confidence, minimum, financial=False, irreversible=False, risk_score=risk_score)
    if requirement.required and not approved:
        return AutonomyPolicyDecision(False, True, safe.action, requirement.reason, conf.confidence, conf.required_confidence)
    return AutonomyPolicyDecision(conf.allowed, False, safe.action, conf.reason, conf.confidence, conf.required_confidence)


def may_execute(action: str, confidence: float, minimum: float, financial: bool = False) -> bool:
    return evaluate_autonomy(action, confidence, minimum, financial=financial).allowed
