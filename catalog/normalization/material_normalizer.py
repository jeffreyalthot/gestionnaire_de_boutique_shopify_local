from __future__ import annotations


class MaterialNormalizer:
    MAP = {"stainless steel": "Stainless Steel", "inox": "Stainless Steel", "acier inoxydable": "Stainless Steel",
           "pp": "Polypropylene", "polypropylene": "Polypropylene", "abs": "ABS Plastic",
           "cotton": "Cotton", "coton": "Cotton", "silicone": "Silicone", "wood": "Wood", "bois": "Wood"}

    def normalize(self, value: str) -> str:
        key = " ".join(value.casefold().split())
        return self.MAP.get(key, value.strip().title()[:100] or "Unspecified")
