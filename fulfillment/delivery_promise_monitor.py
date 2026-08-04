from __future__ import annotations

from datetime import datetime, timezone


class DeliveryPromiseMonitor:
    def inspect(self, *, promised_latest: str, delivered_at: str = "", current_status: str = "") -> dict[str, object]:
        now = datetime.now(timezone.utc)
        try: promise = datetime.fromisoformat(promised_latest.replace("Z", "+00:00"))
        except ValueError: return {"status": "invalid_promise", "late": False}
        delivered = None
        if delivered_at:
            try: delivered = datetime.fromisoformat(delivered_at.replace("Z", "+00:00"))
            except ValueError: pass
        reference = delivered or now
        late = reference > promise and current_status not in {"cancelled", "returned"}
        return {"late": late, "days_late": max(0, (reference.date() - promise.date()).days),
                "delivered": delivered is not None, "status": "late" if late else "on_time"}
