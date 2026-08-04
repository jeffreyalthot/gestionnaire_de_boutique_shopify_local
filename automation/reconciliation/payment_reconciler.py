from __future__ import annotations

from typing import Any

from automation.reconciliation.persistent_reconciler import PersistentReconciler


class PaymentReconciler(PersistentReconciler):
    """Persistent reconciler for payments records."""

    default_key = "id"

    def __init__(self, db: Any, *, maximum_differences: int = 500) -> None:
        super().__init__("payments", db, maximum_differences=maximum_differences)
