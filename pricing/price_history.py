from __future__ import annotations

import json
from uuid import uuid4
from infrastructure.database.engine import Database, utcnow


class PriceHistory:
    def __init__(self, db: Database) -> None: self.db=db
    def record(self, entity_type: str, entity_id: str, *, price_cad: float, landed_cost_cad: float=0, source: str="", metadata: dict[str,object] | None=None) -> str:
        margin=(price_cad-landed_cost_cad)/max(0.01,price_cad)*100
        row_id=str(uuid4())
        self.db.execute("INSERT INTO price_snapshots(id,entity_type,entity_id,price_cad,landed_cost_cad,margin_percent,source,metadata_json,observed_at) VALUES(?,?,?,?,?,?,?,?,?)",
                        (row_id,entity_type,entity_id,price_cad,landed_cost_cad,margin,source,json.dumps(metadata or {},sort_keys=True,default=str),utcnow()))
        return row_id
    def latest(self, entity_type: str, entity_id: str) -> dict[str,object] | None:
        return self.db.query_one("SELECT * FROM price_snapshots WHERE entity_type=? AND entity_id=? ORDER BY observed_at DESC,id DESC LIMIT 1",(entity_type,entity_id))
    def series(self, entity_type: str, entity_id: str, limit: int=100) -> list[dict[str,object]]:
        return self.db.query("SELECT * FROM price_snapshots WHERE entity_type=? AND entity_id=? ORDER BY observed_at DESC LIMIT ?",(entity_type,entity_id,max(1,min(limit,1000))))
