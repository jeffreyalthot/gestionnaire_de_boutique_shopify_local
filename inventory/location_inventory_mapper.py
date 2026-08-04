from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class LocationMapping:
    external: str
    internal: str
    mapped: bool
    fallback_used: bool
    reason: str
    def as_dict(self):return asdict(self)

class LocationInventoryMapper:
    def __init__(self,mappings: dict[str,str]|None=None,*,fallback: str="default") -> None:self.mappings={str(k).strip():str(v).strip() for k,v in (mappings or {}).items()};self.fallback=fallback
    def map(self,external_location: str) -> str:return self.resolve(external_location).internal
    def resolve(self,external_location: str) -> LocationMapping:
        external=str(external_location).strip();internal=self.mappings.get(external)
        if internal:return LocationMapping(external,internal,True,False,"mapped")
        if external:return LocationMapping(external,external,False,False,"identity")
        return LocationMapping(external,self.fallback,False,True,"fallback")
    def reverse(self,internal_location: str) -> tuple[str,...]:return tuple(sorted(k for k,v in self.mappings.items() if v==internal_location))
    def audit(self) -> dict[str,object]:
        duplicates={value:keys for value in set(self.mappings.values()) if len(keys:=self.reverse(value))>1};return {"mappings":len(self.mappings),"duplicate_targets":duplicates,"fallback":self.fallback}
