from __future__ import annotations

from typing import Any

from automation.reconciliation.persistent_reconciler import PersistentReconciler


class ProductMediaReconciler(PersistentReconciler):
    """Persistent reconciler for product media records."""

    default_key = "id"

    def __init__(self, db: Any, *, maximum_differences: int = 500) -> None:
        super().__init__("product_media", db, maximum_differences=maximum_differences)
