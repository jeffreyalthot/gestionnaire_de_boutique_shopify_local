from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class AlibabaApiProfile:
    name: str
    methods: frozenset[str]
    mutating_methods: frozenset[str]
    payment_enabled: bool=False
    def allows(self,method: str,*,mutation: bool=False)->bool:
        return method in self.methods and (not mutation or method in self.mutating_methods)
