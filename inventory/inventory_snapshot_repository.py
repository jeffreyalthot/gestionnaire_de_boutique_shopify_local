from infrastructure.database.engine import Database, utcnow
from inventory.inventory_position import InventoryPosition


class InventorySnapshotRepository:
    def __init__(self, db: Database) -> None: self.db=db
    def upsert(self, p: InventoryPosition) -> None:
        self.db.execute("INSERT INTO inventory_positions(sku,location_id,on_hand,reserved,safety_stock,incoming,supplier_available,updated_at) VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(sku,location_id) DO UPDATE SET on_hand=excluded.on_hand,reserved=excluded.reserved,safety_stock=excluded.safety_stock,incoming=excluded.incoming,supplier_available=excluded.supplier_available,updated_at=excluded.updated_at",
                        (p.sku,p.location_id,p.on_hand,p.reserved,p.safety_stock,p.incoming,p.supplier_available,utcnow()))
    def get(self, sku: str, location_id: str="default") -> InventoryPosition | None:
        row=self.db.query_one("SELECT * FROM inventory_positions WHERE sku=? AND location_id=?",(sku,location_id))
        return InventoryPosition(**{k:row[k] for k in ("sku","on_hand","reserved","safety_stock","incoming","supplier_available","location_id")}) if row else None
    def list_low_stock(self) -> list[InventoryPosition]:
        rows=self.db.query("SELECT * FROM inventory_positions WHERE on_hand-reserved<=safety_stock ORDER BY sku")
        return [InventoryPosition(**{k:r[k] for k in ("sku","on_hand","reserved","safety_stock","incoming","supplier_available","location_id")}) for r in rows]
