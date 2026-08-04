from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AddressQualityResult:
    valid: bool
    score: float
    normalized: dict[str, str]
    issues: tuple[str, ...]


class AddressQuality:
    REQUIRED = ("address1", "city", "country_code")

    def evaluate(self, address: dict[str, object]) -> AddressQualityResult:
        normalized = {str(k): " ".join(str(v or "").strip().split()) for k, v in address.items()}
        issues: list[str] = []
        for field in self.REQUIRED:
            if not normalized.get(field):
                issues.append(f"missing_{field}")
        postal = normalized.get("postal_code", normalized.get("zip", "")).upper()
        country = normalized.get("country_code", "").upper()
        if country == "CA" and postal and not re.fullmatch(r"[A-Z]\d[A-Z][ -]?\d[A-Z]\d", postal):
            issues.append("invalid_canadian_postal_code")
        if country == "US" and postal and not re.fullmatch(r"\d{5}(?:-\d{4})?", postal):
            issues.append("invalid_us_zip")
        if len(normalized.get("address1", "")) > 120:
            issues.append("address_too_long")
        if any(ord(c) < 32 for value in normalized.values() for c in value):
            issues.append("control_character")
        score = max(0.0, 1.0 - 0.2 * len(set(issues)))
        return AddressQualityResult(not issues, round(score, 4), normalized, tuple(sorted(set(issues))))
