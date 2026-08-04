from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class Product:
    id: str
    title: str
    supplier_product_id: str
    shopify_product_id: str = ""
    status: str = "draft"
    score: float = 0.0
