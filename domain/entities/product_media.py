from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class ProductMedia:
    id: str
    product_id: str
    url: str
    alt_text: str = ""
