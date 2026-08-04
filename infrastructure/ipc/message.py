from __future__ import annotations
from dataclasses import asdict,dataclass,field
from datetime import datetime,timezone
from typing import Any
from uuid import uuid4
@dataclass(frozen=True)
class IpcMessage:
    type: str; payload: dict[str,Any]; id: str=field(default_factory=lambda:str(uuid4())); created_at: str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat())
    def as_dict(self): return asdict(self)
