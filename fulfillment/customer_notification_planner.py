from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class NotificationPlan:
    send: bool
    template: str
    reason: str
    priority: str
    channels: tuple[str, ...]
    deduplication_key: str
    context: dict[str, object]
    planned_at: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class CustomerNotificationPlanner:
    TEMPLATES = {
        "label_created": "shipment_confirmed",
        "in_transit": "shipment_moving",
        "out_for_delivery": "out_for_delivery",
        "delivered": "delivered",
        "exception": "shipping_exception",
        "lost": "lost_package_review",
        "undeliverable": "address_problem",
    }
    HIGH_PRIORITY = {"exception", "lost", "undeliverable"}

    def build_plan(
        self,
        previous_status: str,
        current_status: str,
        *,
        customer_opted_in: bool = True,
        order_id: str = "",
        tracking_number: str = "",
        language: str = "fr-CA",
        email_available: bool = True,
        sms_available: bool = False,
    ) -> NotificationPlan:
        current = str(current_status).strip().lower()
        previous = str(previous_status).strip().lower()
        channels = tuple(channel for channel, available in (("email", email_available), ("sms", sms_available)) if available)
        if not customer_opted_in:
            return NotificationPlan(False, "", "customer_opt_out", "none", (), "", {}, datetime.now(timezone.utc).isoformat())
        if current == previous:
            return NotificationPlan(False, "", "no_status_change", "none", (), "", {}, datetime.now(timezone.utc).isoformat())
        template = self.TEMPLATES.get(current, "")
        reason = "status_change" if template else "no_template"
        key = f"shipment-notification:{order_id}:{current}:{tracking_number}"
        return NotificationPlan(
            send=bool(template and channels),
            template=template,
            reason=reason if channels else "no_available_channel",
            priority="high" if current in self.HIGH_PRIORITY else "normal",
            channels=channels,
            deduplication_key=key if template else "",
            context={"order_id": order_id, "tracking_number": tracking_number, "status": current, "language": language},
            planned_at=datetime.now(timezone.utc).isoformat(),
        )

    def plan(self, previous_status: str, current_status: str, *, customer_opted_in: bool = True) -> dict[str, object]:
        result = self.build_plan(previous_status, current_status, customer_opted_in=customer_opted_in).as_dict()
        return {"send": result["send"], "template": result["template"], "reason": result["reason"]}
