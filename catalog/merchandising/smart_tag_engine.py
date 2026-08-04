from __future__ import annotations

import re


class SmartTagEngine:
    def build(self, product: dict[str, object]) -> tuple[str, ...]:
        tags = {str(product.get("category", "general")).casefold().replace(" ", "-")}
        if float(product.get("margin_percent", 0.0) or 0.0) >= 50: tags.add("high-margin")
        if int(product.get("stock", 0) or 0) <= 5: tags.add("low-stock")
        if float(product.get("score", 0.0) or 0.0) >= 0.85: tags.add("featured-candidate")
        for value in dict(product.get("attributes") or {}).values():
            clean = re.sub(r"[^a-z0-9-]+", "-", str(value).casefold()).strip("-")
            if clean: tags.add(clean[:40])
        return tuple(sorted(tags))
