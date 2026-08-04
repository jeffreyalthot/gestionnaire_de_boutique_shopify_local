from __future__ import annotations

from typing import Any

from automation.reconciliation.persistent_reconciler import PersistentReconciler


class RefundReconciler(PersistentReconciler):
    """Persistent reconciler for refunds records."""

    default_key = "id"

    def __init__(self, db: Any, *, maximum_differences: int = 500) -> None:
        super().__init__("refunds", db, maximum_differences=maximum_differences)
