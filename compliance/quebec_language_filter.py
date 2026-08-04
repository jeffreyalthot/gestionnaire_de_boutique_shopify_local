from __future__ import annotations

from compliance.base import ComplianceFinding, result


class QuebecLanguageFilter:
    def evaluate(self, product: dict[str, object], *, market_enabled: bool = True):
        if not market_enabled:
            return result()
        findings = []
        if not str(product.get("title_fr", "")).strip():
            findings.append(ComplianceFinding("french_title_missing", "error", "Titre français absent pour le marché configuré.", True))
        if len(str(product.get("description_fr", "")).strip()) < 40:
            findings.append(ComplianceFinding("french_description_missing", "error", "Description française insuffisante.", True))
        if product.get("instructions_required") and not product.get("instructions_fr"):
            findings.append(ComplianceFinding("french_instructions_missing", "error", "Instructions françaises absentes.", True))
        return result(*findings)
