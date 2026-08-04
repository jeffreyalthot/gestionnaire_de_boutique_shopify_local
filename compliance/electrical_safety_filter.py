from __future__ import annotations

from compliance.base import ComplianceFinding, result


class ElectricalSafetyFilter:
    def evaluate(self, product: dict[str, object]):
        powered = bool(product.get("mains_powered", False))
        if not powered:
            return result()
        findings = []
        voltage = float(product.get("voltage", 0.0) or 0.0)
        certifications = {str(item).casefold() for item in product.get("certifications", ())}
        if voltage <= 0:
            findings.append(ComplianceFinding("voltage_missing", "error", "Tension nominale requise.", True))
        if not certifications.intersection({"csa", "ulc", "etl", "ul", "ce"}):
            findings.append(ComplianceFinding("electrical_evidence_missing", "critical", "Preuve de conformité électrique requise.", True))
        return result(*findings)
