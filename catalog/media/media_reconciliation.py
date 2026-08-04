from __future__ import annotations

from automation.reconciliation.base_reconciler import BaseReconciler


class MediaReconciliation(BaseReconciler):
    def __init__(self) -> None:
        super().__init__("product_media")

    def compare(self, local: list[dict[str, object]], remote: list[dict[str, object]]):
        return self.reconcile(local, remote, key="sha256")
