from __future__ import annotations
from dataclasses import asdict,dataclass,replace

@dataclass(frozen=True,slots=True)
class InventoryPolicy:
    allow_backorder: bool=False
    allow_preorder: bool=False
    safety_stock: int=1
    stale_after_seconds: int=900
    maximum_backorders: int=100
    maximum_preorder_days: int=180
    pause_sales_on_stale: bool=True
    supplier_fallback: bool=False
    def __post_init__(self):
        if self.safety_stock<0 or self.stale_after_seconds<=0:raise ValueError("politique inventaire invalide")
    def update(self,**changes: object) -> "InventoryPolicy":return replace(self,**changes)
    def as_dict(self):return asdict(self)
