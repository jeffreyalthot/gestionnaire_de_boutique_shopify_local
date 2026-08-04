from __future__ import annotations


def map_tracking(data: dict[str, object]) -> dict[str, object]:
    events = data.get("events") or data.get("trackingList") or []
    mapped = [dict(item) for item in events if isinstance(item, dict)] if isinstance(events, list) else []
    mapped.sort(key=lambda item: str(item.get("time", item.get("eventTime", ""))))
    return {
        "carrier": str(data.get("carrier") or data.get("logisticsCompany") or ""),
        "tracking_number": str(data.get("trackingNumber") or data.get("logisticsBillNo") or ""),
        "tracking_url": str(data.get("trackingUrl") or ""),
        "events": mapped,
        "status": str(data.get("status") or "").lower(),
        "last_event": mapped[-1] if mapped else None,
    }
