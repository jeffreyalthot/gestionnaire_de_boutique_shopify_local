from __future__ import annotations

from dataclasses import asdict, dataclass

from infrastructure.database.engine import Database, utcnow


@dataclass(frozen=True, slots=True)
class CancellationResult:
    order_id: str
    cancelled: bool
    previous_status: str
    status: str
    reason: str
    released_reservations: int
    supplier_action: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class CancellationHandler:
    CANCELLABLE = {"pending", "batched", "planned", "approval_required", "retry"}

    def __init__(self, db: Database) -> None:
        self.db = db

    def cancel(
        self,
        order_id: str,
        reason: str,
        *,
        actor: str = "system",
        release_inventory: bool = True,
    ) -> CancellationResult:
        row = self.db.query_one("SELECT procurement_status FROM orders WHERE id=?", (order_id,))
        if not row:
            raise KeyError(order_id)
        previous = str(row["procurement_status"])
        if previous not in self.CANCELLABLE:
            result = CancellationResult(order_id, False, previous, previous, reason, 0, "manual_review")
            self.db.insert_audit("procurement_cancel_rejected", actor, result.as_dict())
            return result

        updated = self.db.execute(
            "UPDATE orders SET procurement_status='cancelled',updated_at=? "
            "WHERE id=? AND procurement_status=?",
            (utcnow(), order_id, previous),
        )
        released = 0
        if updated and release_inventory:
            lines = self.db.query("SELECT sku,quantity FROM order_lines WHERE order_id=?", (order_id,))
            for line in lines:
                released += self.db.execute(
                    "UPDATE inventory_positions SET reserved=MAX(0,reserved-?),updated_at=? WHERE sku=?",
                    (max(0, int(line["quantity"])), utcnow(), str(line["sku"])),
                )
        result = CancellationResult(
            order_id=order_id,
            cancelled=bool(updated),
            previous_status=previous,
            status="cancelled" if updated else previous,
            reason=str(reason).strip() or "unspecified",
            released_reservations=released,
            supplier_action="none",
        )
        self.db.insert_audit("procurement_cancel", actor, result.as_dict())
        return result


def cancel_pending_order(db: Database, order_id: str, reason: str) -> None:
    CancellationHandler(db).cancel(order_id, reason)
