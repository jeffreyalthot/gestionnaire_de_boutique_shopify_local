from __future__ import annotations

import re


class BrandNormalizer:
    GENERIC = {"no brand", "unbranded", "generic", "none", "n/a", "无品牌"}

    def normalize(self, brand: str, *, authorized_brands: set[str] | None = None) -> dict[str, object]:
        clean = " ".join(brand.split()).strip()
        if clean.casefold() in self.GENERIC or not clean:
            return {"brand": "Generic", "authorized": True, "generic": True}
        clean = re.sub(r"[^\w .&'-]+", "", clean)[:100]
        authorized = authorized_brands is None or clean.casefold() in {item.casefold() for item in authorized_brands}
        return {"brand": clean, "authorized": authorized, "generic": False}
