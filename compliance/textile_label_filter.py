from __future__ import annotations

from compliance.base import ComplianceFinding, result


class TextileLabelFilter:
    def evaluate(self, product: dict[str, object]):
        if str(product.get("category", "")).casefold() not in {"apparel", "textile", "clothing", "bedding"}:
            return result()
        findings = []
        composition = product.get("fiber_composition")
        if not composition:
            findings.append(ComplianceFinding("fiber_composition_missing", "error", "Composition textile absente.", True))
        if not product.get("care_instructions"):
            findings.append(ComplianceFinding("care_instructions_missing", "warning", "Instructions d'entretien absentes."))
        if not product.get("country_of_origin"):
            findings.append(ComplianceFinding("origin_missing", "error", "Pays d'origine absent.", True))
        return result(*findings)
