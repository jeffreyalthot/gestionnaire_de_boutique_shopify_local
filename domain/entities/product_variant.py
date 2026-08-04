from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class ProductVariant:
    id: str
    product_id: str
    sku: str
    supplier_sku_id: str
    price_cad: Decimal = Decimal("0")
    stock: int = 0
