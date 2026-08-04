from __future__ import annotations

import json
from typing import Any, Iterable

from analytics.event_facts import EventFact
from analytics.metric_dimensions import normalize_dimensions


class AnalyticsCollector:
    def __init__(self, db: Any, *, max_batch: int = 250) -> None:
        self.db = db
        self.max_batch = max(1, min(max_batch, 1000))

    def record(self, fact: EventFact) -> None:
        self.db.execute(
            "INSERT INTO metric_facts(id,metric,value,dimensions_json,observed_at) VALUES(?,?,?,?,?)",
            (fact.id, fact.metric[:100], float(fact.value), json.dumps(normalize_dimensions(fact.dimensions), ensure_ascii=False), fact.observed_at),
        )

    def record_many(self, facts: Iterable[EventFact]) -> int:
        count = 0
        for fact in facts:
            if count >= self.max_batch:
                break
            self.record(fact)
            count += 1
        return count

    def series(self, metric: str, *, limit: int = 500) -> list[dict[str, Any]]:
        rows = self.db.query(
            "SELECT value,dimensions_json,observed_at FROM metric_facts WHERE metric=? ORDER BY observed_at DESC LIMIT ?",
            (metric, max(1, min(limit, 5000))),
        )
        for row in rows:
            row["dimensions"] = json.loads(row.pop("dimensions_json"))
        return rows
