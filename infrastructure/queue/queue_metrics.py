from __future__ import annotations
from typing import Any
class QueueMetrics:
    def __init__(self,db: Any)->None: self.db=db
    def snapshot(self)->dict[str,int]:
        rows=self.db.query('SELECT status,COUNT(*) count FROM tasks GROUP BY status')
        result={row['status']:int(row['count']) for row in rows}; result['total']=sum(result.values()); return result
