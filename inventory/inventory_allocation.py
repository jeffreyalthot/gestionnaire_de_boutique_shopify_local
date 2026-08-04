from __future__ import annotations

from dataclasses import dataclass
from infrastructure.database.engine import Database, utcnow
from inventory.inventory_position import InventoryPosition


@dataclass(frozen=True, slots=True)
class AllocationResult:
    allocated: bool
    sku: str
    quantity: int
    available_after: int
    reason: str


class InventoryAllocation:
    def __init__(self, db: Database) -> None: self.db=db
    def allocate(self, sku: str, quantity: int, location_id: str="default") -> AllocationResult:
        if quantity<=0: return AllocationResult(False,sku,quantity,0,"invalid_quantity")
        with self.db.transaction() as conn:
            row=conn.execute("SELECT * FROM inventory_positions WHERE sku=? AND location_id=?",(sku,location_id)).fetchone()
            if row is None: return AllocationResult(False,sku,quantity,0,"unknown_sku")
            position=InventoryPosition(**{k:row[k] for k in ("sku","on_hand","reserved","safety_stock","incoming","supplier_available","location_id")})
            if position.available<quantity: return AllocationResult(False,sku,quantity,position.available,"insufficient_stock")
            conn.execute("UPDATE inventory_positions SET reserved=reserved+?,updated_at=? WHERE sku=? AND location_id=?",(quantity,utcnow(),sku,location_id))
            return AllocationResult(True,sku,quantity,position.available-quantity,"allocated")
    def release(self, sku: str, quantity: int, location_id: str="default") -> int:
        self.db.execute("UPDATE inventory_positions SET reserved=MAX(0,reserved-?),updated_at=? WHERE sku=? AND location_id=?",(max(0,quantity),utcnow(),sku,location_id))
        row=self.db.query_one("SELECT reserved FROM inventory_positions WHERE sku=? AND location_id=?",(sku,location_id))
        return int(row["reserved"]) if row else 0
