from __future__ import annotations

import re


class RefundRequestClassifier:
    PATTERNS = {
        "damaged_item": (r"damag", r"broken", r"cass[ée]"),
        "wrong_item": (r"wrong item", r"mauvais article"),
        "missing_item": (r"missing", r"manquant"),
        "late_delivery": (r"late", r"retard"),
        "buyer_remorse": (r"changed my mind", r"plus besoin"),
    }

    def classify(self, text: str) -> tuple[str, float]:
        lower = text.lower()
        for category, patterns in self.PATTERNS.items():
            if any(re.search(pattern, lower) for pattern in patterns):
                return category, 0.9
        return "other", 0.4
