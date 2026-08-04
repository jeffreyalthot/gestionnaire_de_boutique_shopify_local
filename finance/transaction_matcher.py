from __future__ import annotations

from datetime import datetime


class TransactionMatcher:
    def score(self, expected: dict[str, object], actual: dict[str, object]) -> float:
        amount_diff = abs(float(expected.get("amount", 0.0)) - float(actual.get("amount", 0.0)))
        amount_base = max(1.0, abs(float(expected.get("amount", 0.0))))
        amount_score = max(0.0, 1.0 - amount_diff / amount_base)
        reference_score = 1.0 if str(expected.get("reference", "")) and str(expected.get("reference")) == str(actual.get("reference")) else 0.0
        currency_score = 1.0 if str(expected.get("currency", "CAD")) == str(actual.get("currency", "CAD")) else 0.0
        date_score = 0.0
        try:
            left = datetime.fromisoformat(str(expected.get("date", "")))
            right = datetime.fromisoformat(str(actual.get("date", "")))
            date_score = max(0.0, 1.0 - abs((left - right).days) / 7)
        except ValueError:
            pass
        return round(0.55 * amount_score + 0.25 * reference_score + 0.10 * currency_score + 0.10 * date_score, 6)

    def best(self, expected: dict[str, object], candidates: list[dict[str, object]], minimum: float = 0.80):
        ranked = sorted(((self.score(expected, item), item) for item in candidates), key=lambda pair: -pair[0])
        if not ranked or ranked[0][0] < minimum:
            return None
        return {"score": ranked[0][0], "transaction": ranked[0][1]}
