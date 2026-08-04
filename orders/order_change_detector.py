from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json


@dataclass(frozen=True, slots=True)
class OrderChangeSet:
    changes: dict[str, tuple[object, object]]
    material: bool
    procurement_recheck: bool
    fingerprint: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class OrderChangeDetector:
    TRACKED = ("financial_status", "fulfillment_status", "total_amount", "shipping_address", "lines")
    MATERIAL = frozenset({"financial_status", "total_amount", "shipping_address", "lines"})

    def changes(self, before: dict[str, object], after: dict[str, object]) -> dict[str, tuple[object, object]]:
        return self.detect(before, after).changes

    def detect(self, before: dict[str, object], after: dict[str, object]) -> OrderChangeSet:
        changes = {key: (before.get(key), after.get(key)) for key in self.TRACKED if before.get(key) != after.get(key)}
        material = bool(self.MATERIAL.intersection(changes))
        procurement_recheck = bool({"total_amount", "shipping_address", "lines"}.intersection(changes))
        fingerprint = sha256(json.dumps(changes, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24]
        return OrderChangeSet(changes, material, procurement_recheck, fingerprint)
