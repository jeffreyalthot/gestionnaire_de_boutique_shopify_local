from __future__ import annotations

from collections import defaultdict
from typing import Iterable


class ProductCohort:
    def group(self, products: Iterable[dict[str, object]]) -> dict[str, list[str]]:
        groups: dict[str, list[str]] = defaultdict(list)
        for item in products:
            key = str(item.get("category") or item.get("status") or "uncategorized")
            groups[key].append(str(item.get("id", "")))
        return {key: sorted(value) for key, value in sorted(groups.items())}
