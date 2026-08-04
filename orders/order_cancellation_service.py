from datetime import datetime, timezone

from orders.cancellation_window import CancellationWindow


class OrderCancellationService:
    def __init__(self, window: CancellationWindow | None=None) -> None: self.window=window or CancellationWindow()
    def evaluate(self, *, created_at: datetime, financial_status: str, supplier_status: str) -> tuple[bool,str]:
        if financial_status in {"refunded","voided"}: return False,"already_closed"
        if supplier_status not in {"pending","planned",""}: return False,"supplier_order_started"
        try: allowed=self.window.allowed(created_at)
        except TypeError: allowed=self.window.can_cancel(created_at, datetime.now(timezone.utc))
        return (True,"within_window") if allowed else (False,"window_expired")
