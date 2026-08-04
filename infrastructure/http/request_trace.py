from __future__ import annotations
from dataclasses import asdict,dataclass
from datetime import datetime,timezone
from uuid import uuid4
@dataclass(frozen=True)
class RequestTrace:
    id: str; service: str; operation: str; started_at: str
    @classmethod
    def start(cls,service: str,operation: str): return cls(str(uuid4()),service,operation,datetime.now(timezone.utc).isoformat())
    def headers(self): return {'X-Request-ID':self.id}
    def as_dict(self): return asdict(self)
