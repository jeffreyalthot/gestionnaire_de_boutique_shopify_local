from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Any


@dataclass(frozen=True)
class EvidenceItem:
    kind: str
    value: str
    digest: str


class ChargebackEvidenceBuilder:
    allowed_kinds = {'order', 'payment', 'tracking', 'delivery', 'customer_message', 'policy'}

    def build(self, evidence: dict[str, Any]) -> tuple[EvidenceItem, ...]:
        items: list[EvidenceItem] = []
        for kind in sorted(evidence):
            if kind not in self.allowed_kinds or evidence[kind] in (None, '', [], {}):
                continue
            value = str(evidence[kind])[:10000]
            items.append(EvidenceItem(kind, value, sha256(value.encode('utf-8')).hexdigest()))
        return tuple(items)
