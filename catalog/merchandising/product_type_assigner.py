from __future__ import annotations

import re


class ProductTypeAssigner:
    def assign(self, title: str, attributes: dict[str, object], mapping: dict[str, str]) -> str:
        haystack = " ".join([title, *[f"{k} {v}" for k, v in attributes.items()]]).casefold()
        for pattern, product_type in mapping.items():
            if re.search(pattern, haystack, re.IGNORECASE):
                return product_type[:100]
        return "General"
