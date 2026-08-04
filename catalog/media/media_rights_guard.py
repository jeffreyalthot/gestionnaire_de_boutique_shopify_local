from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RightsDecision:
    allowed: bool
    status: str
    reason: str


class MediaRightsGuard:
    def evaluate(self, metadata: dict[str, object]) -> RightsDecision:
        if metadata.get("explicitly_forbidden"):
            return RightsDecision(False, "forbidden", "supplier_forbids_reuse")
        if metadata.get("license") in {"supplier_authorized", "owned", "public_domain"}:
            return RightsDecision(True, "verified", str(metadata.get("license")))
        if metadata.get("supplier_media") and metadata.get("product_authorized"):
            return RightsDecision(True, "supplier_authorized", "authorized_product_media")
        return RightsDecision(False, "unverified", "rights_evidence_required")
