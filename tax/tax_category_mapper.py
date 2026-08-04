from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class TaxCategoryDecision:
    category: str
    taxable: bool
    confidence: float
    matched_keyword: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class TaxCategoryMapper:
    RULES = {
        "food": ("food", "grocery", "aliment", "snack"),
        "clothing": ("shirt", "apparel", "clothing", "dress", "pants", "vêtement"),
        "digital": ("digital", "download", "software", "ebook"),
        "medical": ("medical", "health", "device", "médical"),
        "book": ("book", "livre"),
    }

    def map(self, category: str) -> str:
        return self.resolve(category).category

    def resolve(self, category: str, *, title: str = "", tags: tuple[str, ...] = ()) -> TaxCategoryDecision:
        haystack = " ".join((str(category), str(title), *map(str, tags))).lower()
        matches = [(name, keyword) for name, keywords in self.RULES.items() for keyword in keywords if keyword in haystack]
        if not matches:
            return TaxCategoryDecision("general", True, .5, "")
        name, keyword = matches[0]
        return TaxCategoryDecision(name, name not in {"medical"}, min(1.0, .65 + .1 * len(matches)), keyword)
