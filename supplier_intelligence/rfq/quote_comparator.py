from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class QuoteScore:
    quote: dict[str, Any]
    score: float
    issues: tuple[str, ...]


class QuoteComparator:
    def evaluate(self, quote: dict[str, object]) -> QuoteScore:
        issues: list[str] = []
        landed = float(quote.get("landed_unit_cad", 0) or 0)
        lead = float(quote.get("lead_time_days", 999) or 999)
        supplier = max(0.0, min(1.0, float(quote.get("supplier_score", 0) or 0)))
        quality = max(0.0, min(1.0, float(quote.get("quality_score", supplier) or 0)))
        moq = max(1, int(quote.get("moq", 1) or 1))
        if landed <= 0:
            issues.append("invalid_landed_cost")
        if lead <= 0 or lead > 180:
            issues.append("invalid_lead_time")
        if not (quote.get("supplier_id") or quote.get("supplier")):
            issues.append("missing_supplier")
        cost_score = 1 / (1 + max(0.0, landed))
        lead_score = max(0.0, 1 - lead / 180)
        moq_score = 1 / (1 + max(0, moq - 1) / 100)
        score = (
            0.35 * cost_score
            + 0.20 * lead_score
            + 0.20 * supplier
            + 0.15 * quality
            + 0.10 * moq_score
            - 0.15 * len(issues)
        )
        return QuoteScore(dict(quote), round(max(0.0, min(1.0, score)), 6), tuple(issues))

    def rank(self, quotes: list[dict[str, object]]) -> tuple[dict[str, object], ...]:
        evaluated = [self.evaluate(quote) for quote in quotes]
        ordered = sorted(
            evaluated,
            key=lambda row: (
                bool(row.issues),
                float(row.quote.get("landed_unit_cad", 1e18) or 1e18),
                float(row.quote.get("lead_time_days", 1e18) or 1e18),
                -row.score,
            ),
        )
        return tuple(
            {
                **row.quote,
                "comparison_score": row.score,
                "comparison_issues": row.issues,
            }
            for row in ordered
        )
