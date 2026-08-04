from __future__ import annotations

import re

from compliance.base import ComplianceFinding, result


class EnvironmentalClaimFilter:
    CLAIMS = (r"eco[- ]?friendly", r"green", r"biodegradable", r"carbon neutral", r"recyclable")

    def evaluate(self, text: str, *, evidence_references: tuple[str, ...] = ()):
        claims = tuple(pattern for pattern in self.CLAIMS if re.search(pattern, text, re.IGNORECASE))
        if not claims:
            return result()
        if evidence_references:
            return result(ComplianceFinding("environmental_claim_documented", "info", "Allégation environnementale documentée.", False,
                                            {"claims": claims, "evidence": evidence_references}))
        return result(ComplianceFinding("environmental_claim_unsubstantiated", "error", "Preuve requise pour l'allégation environnementale.", True,
                                        {"claims": claims}))
