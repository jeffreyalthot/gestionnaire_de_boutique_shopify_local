from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable

from automation.policies.policy_engine import ActionPolicy

Handler = Callable[[], Awaitable[dict[str, Any]]]


@dataclass(slots=True)
class ActionPlan:
    name: str
    idempotency_key: str
    policy: ActionPolicy
    handler: Handler
    amount_cad: float = 0.0
    approved: bool = False
    timeout_seconds: float = 60.0
    metadata: dict[str, Any] = field(default_factory=dict)
