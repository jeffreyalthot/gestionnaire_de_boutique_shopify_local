from datetime import datetime,timezone
from infrastructure.database.engine import Database
from inventory.safety_stock import available_for_sale
class InventoryMirror:
    def __init__(self,db: Database,safety_stock: int) -> None: self.db=db; self.safety_stock=safety_stock
    def update_variant(self,product_id: str,supplier_sku_id: str,stock: int) -> int:
        sellable=available_for_sale(stock,self.safety_stock)
        self.db.execute("UPDATE product_variants SET stock=?,updated_at=? WHERE product_id=? AND supplier_sku_id=?",
                        (sellable,datetime.now(timezone.utc).isoformat(),product_id,supplier_sku_id))
        return sellable
