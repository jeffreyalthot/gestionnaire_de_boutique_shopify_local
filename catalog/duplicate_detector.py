from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from difflib import SequenceMatcher


@dataclass(frozen=True, slots=True)
class DuplicateScore:
    similar: bool
    title_score: float
    sku_match: bool
    barcode_match: bool
    reason: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class DuplicateDetector:
    @staticmethod
    def normalize(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()

    def similar(self, a: str, b: str, threshold: float = 0.92) -> bool:
        return self.compare({"title": a}, {"title": b}, threshold=threshold).similar

    def compare(self, first: dict[str, object], second: dict[str, object], *, threshold: float = 0.92) -> DuplicateScore:
        title_score = SequenceMatcher(None, self.normalize(str(first.get("title", ""))), self.normalize(str(second.get("title", "")))).ratio()
        sku_a, sku_b = str(first.get("sku", "")).strip(), str(second.get("sku", "")).strip()
        barcode_a, barcode_b = str(first.get("barcode", "")).strip(), str(second.get("barcode", "")).strip()
        sku_match = bool(sku_a and sku_b and sku_a == sku_b)
        barcode_match = bool(barcode_a and barcode_b and barcode_a == barcode_b)
        similar = barcode_match or sku_match or title_score >= threshold
        reason = "barcode" if barcode_match else ("sku" if sku_match else ("title" if similar else "distinct"))
        return DuplicateScore(similar, round(title_score, 6), sku_match, barcode_match, reason)
