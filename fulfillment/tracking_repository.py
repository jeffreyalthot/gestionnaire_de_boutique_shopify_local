from __future__ import annotations

import json
from typing import Any

from fulfillment.tracking_event import TrackingEvent
from infrastructure.database.engine import utcnow


class TrackingRepository:
    def __init__(self, db: Any) -> None: self.db=db

    def append(self, shipment_id: str, event: TrackingEvent) -> None:
        row=self.db.query_one("SELECT events_json FROM shipments WHERE id=?",(shipment_id,))
        if not row: raise KeyError(shipment_id)
        events=list(json.loads(row["events_json"] or "[]")); events.append(event.as_dict())
        self.db.execute("UPDATE shipments SET events_json=?,status=?,updated_at=? WHERE id=?",
                        (json.dumps(events[-200:],ensure_ascii=False,default=str),event.status,utcnow(),shipment_id))

    def events(self, shipment_id: str) -> tuple[dict[str,Any],...]:
        row=self.db.query_one("SELECT events_json FROM shipments WHERE id=?",(shipment_id,))
        return tuple(json.loads(row["events_json"] or "[]")) if row else ()
