from __future__ import annotations

import hashlib
import hmac
from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class AccessDecision:
    allowed: bool
    principal: str
    permission: str
    reason: str
    evaluated_at: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class AccessControl:
    def __init__(self, role_permissions: dict[str, set[str]] | None = None) -> None:
        self.role_permissions = role_permissions or {
            "viewer": {"status:read", "report:read"},
            "operator": {"status:read", "report:read", "automation:run", "queue:retry"},
            "admin": {"*"},
        }

    def authorize(self, principal: str, roles: list[str] | tuple[str, ...], permission: str) -> AccessDecision:
        permissions = set().union(*(self.role_permissions.get(role, set()) for role in roles))
        allowed = "*" in permissions or permission in permissions
        return AccessDecision(allowed, principal, permission, "granted" if allowed else "permission_denied", datetime.now(timezone.utc).isoformat())

    @staticmethod
    def token_fingerprint(token: str) -> str:
        return hashlib.sha256(str(token).encode()).hexdigest()[:16]


def verify_admin_token(provided: str, configured: str) -> bool:
    return bool(configured) and hmac.compare_digest(str(provided), str(configured))
