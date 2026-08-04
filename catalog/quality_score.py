from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class QualityAssessment:
    score: float
    grade: str
    checks: dict[str, bool]
    issues: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def assess_quality(product: dict[str, object]) -> QualityAssessment:
    checks = {
        "title": bool(str(product.get("title", "")).strip()),
        "description": len(str(product.get("description", "")).strip()) >= 80,
        "images": len(product.get("images", []) or []) >= 3,
        "variants": bool(product.get("skus") or product.get("variants")),
        "price": float(product.get("price", product.get("supplier_cost", 0)) or 0) > 0,
        "supplier": bool(product.get("supplier") or product.get("supplier_id")),
        "stock": int(product.get("stock", 0) or 0) > 0,
    }
    weights = {"title": .12, "description": .14, "images": .18, "variants": .14, "price": .16, "supplier": .14, "stock": .12}
    score = sum(weights[key] for key, passed in checks.items() if passed)
    issues = tuple(key for key, passed in checks.items() if not passed)
    grade = "A" if score >= .90 else ("B" if score >= .80 else ("C" if score >= .70 else ("D" if score >= .60 else "F")))
    return QualityAssessment(round(score, 4), grade, checks, issues)


def quality_score(product: dict[str, object]) -> float:
    return assess_quality(product).score
