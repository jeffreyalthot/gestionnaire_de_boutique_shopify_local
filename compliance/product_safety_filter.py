from __future__ import annotations

from compliance.base import ComplianceFinding, result


class ProductSafetyFilter:
    def evaluate(self, product: dict[str, object]):
        findings = []
        if bool(product.get("sharp_edges", False)) and not product.get("warning_label"):
            findings.append(ComplianceFinding("sharp_edge_warning_missing", "error", "Avertissement requis pour bord tranchant.", True))
        if float(product.get("operating_temperature_c", 0.0) or 0.0) > 60 and not product.get("hot_surface_warning"):
            findings.append(ComplianceFinding("hot_surface_warning_missing", "error", "Avertissement surface chaude requis.", True))
        if bool(product.get("small_parts", False)) and not product.get("age_grade"):
            findings.append(ComplianceFinding("small_parts_age_grade_missing", "error", "Classification d'âge requise.", True))
        if not product.get("traceability_reference"):
            findings.append(ComplianceFinding("traceability_missing", "warning", "Référence de traçabilité fournisseur absente."))
        return result(*findings)
