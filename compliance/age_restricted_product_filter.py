from __future__ import annotations

import re

from compliance.base import ComplianceFinding, result


class AgeRestrictedProductFilter:
    PATTERNS = (r"alcohol", r"tobacco", r"nicotine", r"vape", r"lottery")

    def evaluate(self, text: str, *, age_gate_supported: bool = False):
        matches = tuple(pattern for pattern in self.PATTERNS if re.search(pattern, text, re.IGNORECASE))
        if not matches:
            return result()
        return result(ComplianceFinding("age_restricted", "critical", "Produit possiblement soumis à une restriction d'âge.",
                                        blocking=not age_gate_supported, evidence={"patterns": matches}))
