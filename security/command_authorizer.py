from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuthorizationDecision:
    allowed: bool
    reason: str


class CommandAuthorizer:
    ROLE_ACTIONS = {
        "viewer": {"status", "catalog-review", "order-review", "finance-review"},
        "operator": {"status", "catalog-review", "order-review", "finance-review", "catalog-sync", "inventory-sync", "tracking-sync"},
        "administrator": {"*"},
    }

    def authorize(self, role: str, action: str, *, sensitive: bool = False, approved: bool = False) -> AuthorizationDecision:
        actions=self.ROLE_ACTIONS.get(role, set())
        if "*" not in actions and action not in actions: return AuthorizationDecision(False, "role_denied")
        if sensitive and not approved: return AuthorizationDecision(False, "explicit_approval_required")
        return AuthorizationDecision(True, "allowed")
