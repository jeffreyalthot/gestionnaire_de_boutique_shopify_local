import json
from uuid import uuid4
from infrastructure.database.engine import Database, utcnow


class SqliteMetricsSink:
    def __init__(self, db: Database) -> None: self.db=db
    def write(self, metric: str, value: float, dimensions: dict[str,object] | None=None) -> None:
        self.db.execute("INSERT INTO metric_facts(id,metric,value,dimensions_json,observed_at) VALUES(?,?,?,?,?)",(str(uuid4()),metric,value,json.dumps(dimensions or {},sort_keys=True,default=str),utcnow()))
