from enum import StrEnum

class SupplierStatus(StrEnum):
    UNKNOWN = "unknown"
    APPROVED = "approved"
    REVIEW = "review"
    BLOCKED = "blocked"
