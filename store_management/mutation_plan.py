from __future__ import annotations
from dataclasses import asdict,dataclass
from hashlib import sha256
from typing import Any
@dataclass(frozen=True,slots=True)
class MutationPlan:
    resource: str
    operation: str
    input: dict[str,Any]
    safe: bool=True
    approval_required: bool=False
    warnings: tuple[str,...]=()
    @property
    def idempotency_key(self) -> str:return sha256(f"{self.resource}|{self.operation}|{repr(sorted(self.input.items()))}".encode()).hexdigest()
    def to_dict(self) -> dict[str,Any]:
        out=asdict(self);out["idempotency_key"]=self.idempotency_key;return out

def clean_handle(value: str) -> str:
    import re
    value=re.sub(r"[^a-z0-9-]+","-",value.strip().lower().replace("_","-"));return re.sub(r"-+","-",value).strip("-")
