from __future__ import annotations

from datetime import datetime, timedelta, timezone


class ProductRefreshPlanner:
    def due(self, product: dict[str, object], *, now: datetime | None = None) -> dict[str, object]:
        now = now or datetime.now(timezone.utc)
        raw = str(product.get("updated_at", ""))
        try:
            updated = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            updated = now - timedelta(days=365)
        risk = str(product.get("risk_level", "normal"))
        interval = {"critical": 1, "high": 3, "normal": 14, "low": 30}.get(risk, 14)
        due_at = updated + timedelta(days=interval)
        return {"due": now >= due_at, "due_at": due_at.isoformat(), "interval_days": interval}
