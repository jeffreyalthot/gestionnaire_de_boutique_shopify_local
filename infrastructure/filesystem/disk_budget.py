from __future__ import annotations
import shutil
from dataclasses import asdict,dataclass
from pathlib import Path
@dataclass(frozen=True)
class DiskBudgetSnapshot:
    total: int; used: int; free: int; required_free: int
    @property
    def ok(self)->bool: return self.free>=self.required_free
    def as_dict(self): return {**asdict(self),'ok':self.ok}
class DiskBudget:
    def __init__(self,path: Path,required_free_bytes: int=536870912)->None: self.path=Path(path); self.required=required_free_bytes
    def snapshot(self)->DiskBudgetSnapshot:
        total,used,free=shutil.disk_usage(self.path); return DiskBudgetSnapshot(total,used,free,self.required)
