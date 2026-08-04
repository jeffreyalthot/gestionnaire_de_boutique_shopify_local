from __future__ import annotations

from typing import Any

from automation.reconciliation.persistent_reconciler import PersistentReconciler


class InventoryReconciler(PersistentReconciler):
    """Persistent reconciler for inventory records."""

    default_key = "sku"

    def __init__(self, db: Any, *, maximum_differences: int = 500) -> None:
        super().__init__("inventory", db, maximum_differences=maximum_differences)
