from __future__ import annotations

import re

from compliance.base import ComplianceFinding, result


class IntellectualPropertyFilter:
    RISK_TERMS = (r"replica", r"1:1", r"copy", r"inspired by", r"dupe")

    def evaluate(self, text: str, *, protected_brands: set[str] = frozenset(), authorization_reference: str = ""):
        findings = []
        terms = tuple(pattern for pattern in self.RISK_TERMS if re.search(pattern, text, re.IGNORECASE))
        brands = tuple(sorted(brand for brand in protected_brands if brand.casefold() in text.casefold()))
        if terms:
            findings.append(ComplianceFinding("counterfeit_language", "critical", "Langage associé à une contrefaçon potentielle.", True, {"terms": terms}))
        if brands and not authorization_reference:
            findings.append(ComplianceFinding("protected_brand", "critical", "Autorisation de marque requise.", True, {"brands": brands}))
        return result(*findings)
