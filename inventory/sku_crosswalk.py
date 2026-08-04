from __future__ import annotations
from dataclasses import asdict,dataclass
from infrastructure.database.engine import Database

@dataclass(frozen=True,slots=True)
class SKUMapping:
    sku: str
    product_id: str
    variant_id: str
    supplier_product_id: str
    supplier_sku_id: str
    found: bool
    def as_dict(self):return asdict(self)

class SKUCrosswalk:
    def __init__(self,db: Database) -> None:self.db=db
    def find(self,sku: str) -> dict[str,object]|None:
        return self.db.query_one("SELECT pv.*,p.supplier_product_id FROM product_variants pv JOIN products p ON p.id=pv.product_id WHERE pv.sku=?",(str(sku).strip().upper(),))
    def resolve(self,sku: str) -> SKUMapping:
        row=self.find(sku) or {};return SKUMapping(str(sku).strip().upper(),str(row.get("product_id","")),str(row.get("id",row.get("variant_id",""))),str(row.get("supplier_product_id","")),str(row.get("supplier_sku_id","")),bool(row))
    def find_supplier(self,supplier_sku_id: str) -> tuple[dict[str,object],...]:
        return tuple(self.db.query("SELECT pv.*,p.supplier_product_id FROM product_variants pv JOIN products p ON p.id=pv.product_id WHERE pv.supplier_sku_id=?",(supplier_sku_id,)))
    def audit_duplicates(self) -> tuple[dict[str,object],...]:
        return tuple(self.db.query("SELECT sku,COUNT(*) count FROM product_variants WHERE sku<>'' GROUP BY sku HAVING COUNT(*)>1 ORDER BY count DESC"))
