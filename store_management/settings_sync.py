from __future__ import annotations
from dataclasses import asdict,dataclass
from datetime import datetime,timezone

@dataclass(frozen=True,slots=True)
class SettingChange:
    key: str
    local: object
    remote: object
    safe: bool
    approval_required: bool

@dataclass(frozen=True,slots=True)
class SettingsSyncPlan:
    changes: tuple[SettingChange,...]
    ignored: tuple[str,...]
    generated_at: str
    def as_dict(self):return asdict(self)

class StoreSettingsSync:
    SAFE_FIELDS={"name","email","currency","timezone","weight_unit","order_number_format","customer_accounts"}
    SENSITIVE_FIELDS={"currency","customer_accounts","order_number_format"}
    def diff(self,local: dict[str,object],remote: dict[str,object]) -> dict[str,dict[str,object]]:
        return {change.key:{"local":change.local,"remote":change.remote} for change in self.plan(local,remote).changes}
    def plan(self,local: dict[str,object],remote: dict[str,object]) -> SettingsSyncPlan:
        changes=[]
        for key in sorted(self.SAFE_FIELDS):
            if key in local and local.get(key)!=remote.get(key):changes.append(SettingChange(key,local.get(key),remote.get(key),True,key in self.SENSITIVE_FIELDS))
        ignored=tuple(sorted(set(local)-self.SAFE_FIELDS))
        return SettingsSyncPlan(tuple(changes),ignored,datetime.now(timezone.utc).isoformat())
    def apply(self,remote: dict[str,object],plan: SettingsSyncPlan,*,approved: bool=False) -> dict[str,object]:
        result=dict(remote)
        for change in plan.changes:
            if change.approval_required and not approved:continue
            result[change.key]=change.local
        return result
