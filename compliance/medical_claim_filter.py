from __future__ import annotations

import re

from compliance.base import ComplianceFinding, result


class MedicalClaimFilter:
    CLAIMS = (r"cure[sd]?", r"treats?", r"diagnos", r"prevent(?:s|ion)?", r"heals?",
              r"guaranteed relief", r"clinically proven")

    def evaluate(self, text: str, *, reviewed: bool = False):
        matches = tuple(pattern for pattern in self.CLAIMS if re.search(pattern, text, re.IGNORECASE))
        if not matches:
            return result()
        return result(ComplianceFinding("medical_claim", "critical", "Allégation médicale détectée; revue spécialisée obligatoire.",
                                        blocking=not reviewed, evidence={"patterns": matches}))
