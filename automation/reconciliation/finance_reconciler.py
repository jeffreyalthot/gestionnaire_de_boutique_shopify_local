from __future__ import annotations

from typing import Any

from automation.reconciliation.persistent_reconciler import PersistentReconciler


class FinanceReconciler(PersistentReconciler):
    """Persistent reconciler for finance records."""

    default_key = "transaction_id"

    def __init__(self, db: Any, *, maximum_differences: int = 500) -> None:
        super().__init__("finance", db, maximum_differences=maximum_differences)
