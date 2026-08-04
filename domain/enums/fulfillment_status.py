from enum import StrEnum

class FulfillmentStatus(StrEnum):
    UNFULFILLED = "unfulfilled"
    ON_HOLD = "on_hold"
    IN_PROGRESS = "in_progress"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"
