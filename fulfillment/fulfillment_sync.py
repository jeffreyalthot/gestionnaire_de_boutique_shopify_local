from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from threading import RLock

from fulfillment.tracking_sync import TrackingSync


@dataclass(frozen=True, slots=True)
class FulfillmentSyncResult:
    shipment_id: str
    supplier_order_id: str
    status: str
    changed: bool
    fingerprint: str
    synced_at: str
    tracking: dict[str, object]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class FulfillmentSync:
    def __init__(self, tracking_sync: TrackingSync, maximum_fingerprints: int = 10_000) -> None:
        self.tracking_sync = tracking_sync
        self.maximum_fingerprints = max(100, int(maximum_fingerprints))
        self._fingerprints: dict[str, str] = {}
        self._lock = RLock()

    @staticmethod
    def _fingerprint(tracking: dict[str, object]) -> str:
        import json
        return hashlib.sha256(json.dumps(tracking, sort_keys=True, default=str, separators=(",", ":")).encode()).hexdigest()

    async def synchronize(self, shipment: dict[str, object]) -> FulfillmentSyncResult:
        shipment_id = str(shipment.get("id") or "")
        supplier_order_id = str(shipment.get("supplier_order_id") or "")
        if not shipment_id or not supplier_order_id:
            raise ValueError("shipment id et supplier_order_id requis")
        tracking = dict(await self.tracking_sync.sync(shipment))
        fingerprint = self._fingerprint(tracking)
        with self._lock:
            changed = self._fingerprints.get(shipment_id) != fingerprint
            self._fingerprints[shipment_id] = fingerprint
            if len(self._fingerprints) > self.maximum_fingerprints:
                self._fingerprints.pop(next(iter(self._fingerprints)), None)
        return FulfillmentSyncResult(
            shipment_id=shipment_id,
            supplier_order_id=supplier_order_id,
            status=str(tracking.get("status") or "unknown"),
            changed=changed,
            fingerprint=fingerprint,
            synced_at=datetime.now(timezone.utc).isoformat(),
            tracking=tracking,
        )

    async def execute(self, shipment: dict[str, object]) -> dict[str, object]:
        return (await self.synchronize(shipment)).tracking
