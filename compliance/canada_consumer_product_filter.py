from __future__ import annotations

from compliance.base import ComplianceFinding, result


class CanadaConsumerProductFilter:
    """Contrôles de données configurables; ne remplace pas une évaluation réglementaire."""

    def evaluate(self, product: dict[str, object]):
        findings = []
        category = str(product.get("category", "")).casefold()
        if not str(product.get("manufacturer", "")).strip():
            findings.append(ComplianceFinding("manufacturer_missing", "warning", "Fabricant non documenté."))
        if category in {"toy", "children", "child", "baby"} and not product.get("age_grade"):
            findings.append(ComplianceFinding("age_grade_missing", "error", "Tranche d'âge requise pour ce type de produit.", True))
        if category in {"cosmetic", "food", "supplement"}:
            findings.append(ComplianceFinding("regulated_category_review", "critical", "Revue spécialisée requise.", True,
                                               {"category": category}))
        return result(*findings)
