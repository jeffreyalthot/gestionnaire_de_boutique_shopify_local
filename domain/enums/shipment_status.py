from enum import StrEnum

class ShipmentStatus(StrEnum):
    PENDING = "pending"
    LABEL_CREATED = "label_created"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    EXCEPTION = "exception"
