from __future__ import annotations

from compliance.base import ComplianceFinding, result


class ImageUsageRightsFilter:
    def evaluate(self, metadata: dict[str, object]):
        license_name = str(metadata.get("license", ""))
        authorized = license_name in {"owned", "supplier_authorized", "public_domain"} or bool(metadata.get("written_permission"))
        if authorized:
            return result()
        return result(ComplianceFinding("image_rights_unverified", "critical", "Droits de réutilisation de l'image non prouvés.", True,
                                        {"source": metadata.get("source", "")}))
