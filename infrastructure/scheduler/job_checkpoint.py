from __future__ import annotations
from datetime import datetime,timezone
from typing import Any
class JobCheckpoint:
    def __init__(self,db: Any)->None: self.db=db
    def record(self,name: str,status: str,detail: dict|None=None)->None: self.db.set_value(f'scheduler:{name}',{'status':status,'detail':detail or {},'at':datetime.now(timezone.utc).isoformat()})
    def load(self,name: str): return self.db.get_value(f'scheduler:{name}',None)
