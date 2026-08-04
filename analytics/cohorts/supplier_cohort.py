from __future__ import annotations

from collections import defaultdict
from typing import Iterable


class SupplierCohort:
    def group(self, suppliers: Iterable[dict[str, object]]) -> dict[str, list[str]]:
        groups: dict[str, list[str]] = defaultdict(list)
        for item in suppliers:
            score = float(item.get("score", 0.0))
            risk = "preferred" if score >= 0.85 else ("approved" if score >= 0.65 else "review")
            groups[risk].append(str(item.get("supplier_id", item.get("id", ""))))
        return {key: sorted(value) for key, value in sorted(groups.items())}
