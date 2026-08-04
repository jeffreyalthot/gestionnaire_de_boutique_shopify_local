from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class ThemeSettingsPatch:
    result: dict[str,object]
    changed: tuple[str,...]
    unchanged: tuple[str,...]
    rejected: tuple[str,...]
    def as_dict(self):return asdict(self)

class ThemeSettingsManager:
    def patch(self,current: dict[str,object],changes: dict[str,object],allowed: set[str]) -> dict[str,object]:return self.plan(current,changes,allowed).result
    def plan(self,current: dict[str,object],changes: dict[str,object],allowed: set[str]) -> ThemeSettingsPatch:
        unknown=tuple(sorted(set(changes)-allowed))
        if unknown:raise ValueError(f"paramètres non autorisés: {list(unknown)}")
        result=dict(current);changed=[];unchanged=[]
        for key,value in changes.items():
            if current.get(key)==value:unchanged.append(key)
            else:result[key]=value;changed.append(key)
        return ThemeSettingsPatch(result,tuple(sorted(changed)),tuple(sorted(unchanged)),unknown)
