from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Iterable


class CustomerCohort:
    def group(self, customers: Iterable[dict[str, object]], *, period: str = "month") -> dict[str, list[str]]:
        groups: dict[str, list[str]] = defaultdict(list)
        for item in customers:
            raw = str(item.get("created_at", ""))
            try:
                dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
                key = dt.strftime("%Y-%m" if period == "month" else "%Y-W%W")
            except ValueError:
                key = "unknown"
            groups[key].append(str(item.get("id", item.get("customer_id", ""))))
        return {key: sorted(value) for key, value in sorted(groups.items())}
