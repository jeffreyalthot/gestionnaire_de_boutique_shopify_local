from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InventoryPosition:
    sku: str
    on_hand: int
    reserved: int=0
    safety_stock: int=0
    incoming: int=0
    supplier_available: int | None=None
    location_id: str="default"

    @property
    def available(self) -> int:
        return max(0,self.on_hand-self.reserved-self.safety_stock)

    @property
    def projected(self) -> int:
        return self.available+max(0,self.incoming)
