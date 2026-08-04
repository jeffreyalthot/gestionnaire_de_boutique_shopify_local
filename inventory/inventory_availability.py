from __future__ import annotations
from dataclasses import asdict,dataclass
from inventory.inventory_position import InventoryPosition

@dataclass(frozen=True,slots=True)
class AvailabilityDecision:
    fulfillable: bool
    requested: int
    local_capacity: int
    supplier_capacity: int|None
    shortage: int
    source: str
    reason: str
    def as_dict(self):return asdict(self)

class InventoryAvailability:
    def can_fulfill(self,position: InventoryPosition,quantity: int,*,include_incoming: bool=False) -> bool:return self.evaluate(position,quantity,include_incoming=include_incoming).fulfillable
    def evaluate(self,position: InventoryPosition,quantity: int,*,include_incoming: bool=False,allow_supplier_fallback: bool=False) -> AvailabilityDecision:
        requested=int(quantity);capacity=int(position.projected if include_incoming else position.available);supplier=position.supplier_available;local_ok=requested>0 and capacity>=requested;supplier_ok=allow_supplier_fallback and supplier is not None and supplier>=requested;fulfillable=local_ok or supplier_ok;source="local" if local_ok else "supplier" if supplier_ok else "none";shortage=max(0,requested-capacity);reason="available" if fulfillable else "invalid_quantity" if requested<=0 else "insufficient_stock"
        return AvailabilityDecision(fulfillable,requested,capacity,supplier,shortage,source,reason)
