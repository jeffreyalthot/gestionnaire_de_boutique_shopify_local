from enum import StrEnum

class OrderStatus(StrEnum):
    RECEIVED = "received"
    PAID = "paid"
    RISK_REVIEW = "risk_review"
    QUEUED = "queued"
    PROCURED = "procured"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
