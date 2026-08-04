from enum import StrEnum

class BatchStatus(StrEnum):
    OPEN = "open"
    READY = "ready"
    APPROVAL_REQUIRED = "approval_required"
    SUBMITTING = "submitting"
    SUBMITTED = "submitted"
    PAID = "paid"
    PARTIAL = "partial"
    FAILED = "failed"
