from __future__ import annotations

from typing import Any

from automation.reconciliation.persistent_reconciler import PersistentReconciler


class TrackingReconciler(PersistentReconciler):
    """Persistent reconciler for tracking records."""

    default_key = "tracking_number"

    def __init__(self, db: Any, *, maximum_differences: int = 500) -> None:
        super().__init__("tracking", db, maximum_differences=maximum_differences)
