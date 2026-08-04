from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(slots=True)
class ProjectedOrderState:
    status: str = "unknown"
    held: bool = False
    notes: int = 0
    financial_status: str = ""
    fulfillment_status: str = ""
    procurement_status: str = ""
    tracking_number: str = ""
    last_event: str = ""
    history: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class OrderStateProjector:
    def project(self, events: list[dict[str, object]]) -> dict[str, object]:
        state = ProjectedOrderState()
        for event in sorted(events, key=lambda item: str(item.get("created_at", item.get("at", "")))):
            kind = str(event.get("event_type", event.get("type", "")))
            state.last_event = kind
            state.history.append(kind)
            if kind == "order_held":
                state.held = True; state.status = "held"
            elif kind == "order_released":
                state.held = False; state.status = "pending"
            elif kind == "note":
                state.notes += 1
            elif kind in {"order_cancelled", "cancelled"}:
                state.status = "cancelled"
            elif kind in {"supplier_order_submitted", "procurement_started"}:
                state.procurement_status = "submitted"
            elif kind in {"shipment_created", "tracking_updated"}:
                state.tracking_number = str(event.get("tracking_number", state.tracking_number))
            for field_name in ("financial_status", "fulfillment_status", "procurement_status"):
                if event.get(field_name): setattr(state, field_name, str(event[field_name]))
            if event.get("status"): state.status = str(event["status"])
        return state.as_dict()
