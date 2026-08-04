from enum import StrEnum

class ProductStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"
    OUT_OF_STOCK = "out_of_stock"
    BLOCKED = "blocked"
