from __future__ import annotations

import hashlib
import hmac

from compliance.base import ComplianceFinding, result


class SanctionsFilter:
    """Compare des empreintes normalisées fournies par une source de conformité externe."""

    def __init__(self, salt: str) -> None:
        self.salt = salt.encode("utf-8")

    def fingerprint(self, name: str, country: str = "") -> str:
        normalized = " ".join(f"{name}|{country}".casefold().split())
        return hmac.new(self.salt, normalized.encode("utf-8"), hashlib.sha256).hexdigest()

    def evaluate(self, name: str, country: str, blocked_fingerprints: set[str]):
        digest = self.fingerprint(name, country)
        if digest in blocked_fingerprints:
            return result(ComplianceFinding("sanctions_match", "critical", "Correspondance avec une liste configurée.", True))
        return result()
