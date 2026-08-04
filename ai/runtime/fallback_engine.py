from __future__ import annotations

from dataclasses import asdict, dataclass
import re


@dataclass(frozen=True, slots=True)
class FallbackClassification:
    category: str
    confidence: float
    matched_terms: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class FallbackEngine:
    rules = {
        "refund": ("refund", "rembourse", "money back", "retour d'argent"),
        "shipping": ("tracking", "suivi", "livraison", "delivery", "colis"),
        "cancellation": ("cancel", "annul", "stop order"),
        "damaged": ("damaged", "broken", "endommag", "cassé"),
        "wrong_item": ("wrong item", "incorrect", "mauvais article"),
        "missing_item": ("missing", "manquant", "absent"),
    }

    def classify(self, text: str) -> str:
        return self.classify_with_metadata(text).category

    def classify_with_metadata(self, text: str) -> FallbackClassification:
        lower = re.sub(r"\s+", " ", str(text).lower())
        scored: list[tuple[int, str, tuple[str, ...]]] = []
        for category, terms in self.rules.items():
            matched = tuple(term for term in terms if term in lower)
            if matched:
                scored.append((sum(len(term) for term in matched), category, matched))
        if not scored:
            return FallbackClassification("general", .35, ())
        score, category, matched = max(scored)
        return FallbackClassification(category, min(.95, .55 + score / 100), matched)
