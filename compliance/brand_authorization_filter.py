from __future__ import annotations

from compliance.base import ComplianceFinding, result


class BrandAuthorizationFilter:
    def evaluate(self, brand: str, *, authorized_brands: set[str], generic: bool = False):
        if generic or not brand.strip():
            return result()
        authorized = brand.casefold() in {item.casefold() for item in authorized_brands}
        if authorized:
            return result()
        return result(ComplianceFinding("brand_authorization_missing", "critical",
                                        "Preuve d'autorisation de marque requise.", True, {"brand": brand}))
