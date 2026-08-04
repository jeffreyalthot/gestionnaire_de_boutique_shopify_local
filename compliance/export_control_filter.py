from __future__ import annotations

from compliance.base import ComplianceFinding, result


class ExportControlFilter:
    def evaluate(self, *, destination: str, blocked_destinations: set[str], controlled_classification: str = "",
                 license_reference: str = ""):
        findings = []
        if destination.upper() in {item.upper() for item in blocked_destinations}:
            findings.append(ComplianceFinding("blocked_destination", "critical", "Destination interdite par la politique configurée.", True,
                                               {"destination": destination}))
        if controlled_classification and not license_reference:
            findings.append(ComplianceFinding("export_license_missing", "critical", "Référence d'autorisation requise.", True,
                                               {"classification": controlled_classification}))
        return result(*findings)
