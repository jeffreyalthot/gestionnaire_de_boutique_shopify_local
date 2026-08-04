from __future__ import annotations
from integrations.alibaba.api_profile import AlibabaApiProfile
class AlibabaApiProfileRegistry:
    def __init__(self)->None:self._profiles={}
    def register(self,profile: AlibabaApiProfile)->None:
        if profile.name in self._profiles: raise ValueError('Profil Alibaba dupliqué.')
        self._profiles[profile.name]=profile
    def get(self,name: str)->AlibabaApiProfile:return self._profiles[name]
    def names(self)->tuple[str, ...]:return tuple(sorted(self._profiles))
