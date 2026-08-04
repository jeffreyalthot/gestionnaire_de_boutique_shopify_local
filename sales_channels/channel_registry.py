from __future__ import annotations
from sales_channels.channel_capabilities import ChannelCapabilities
class ChannelRegistry:
    def __init__(self) -> None:self._channels={};self._capabilities={}
    def register(self,name: str,adapter: object,capabilities: ChannelCapabilities | None=None) -> None:
        name=name.strip().lower()
        if not name:raise ValueError("nom du canal requis")
        if name in self._channels:raise ValueError("canal déjà enregistré")
        self._channels[name]=adapter;self._capabilities[name]=capabilities or ChannelCapabilities()
    def get(self,name: str):return self._channels[name.strip().lower()]
    def capabilities(self,name: str) -> ChannelCapabilities:return self._capabilities[name.strip().lower()]
    def names(self) -> tuple[str,...]:return tuple(sorted(self._channels))
    def map_product(self,name: str,product: dict[str,object]) -> dict[str,object]:
        adapter=self.get(name);mapper=getattr(adapter,"map_product",None)
        if not callable(mapper):raise TypeError(f"canal sans map_product: {name}")
        return mapper(product)
    def snapshot(self) -> dict[str,object]:return {name:{"adapter":type(self._channels[name]).__name__,"capabilities":self._capabilities[name].__dict__ if hasattr(self._capabilities[name],'__dict__') else {field:getattr(self._capabilities[name],field) for field in self._capabilities[name].__dataclass_fields__}} for name in self.names()}
