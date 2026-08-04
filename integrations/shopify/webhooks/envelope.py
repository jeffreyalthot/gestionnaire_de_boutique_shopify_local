from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
@dataclass(frozen=True, slots=True)
class ShopifyWebhookEnvelope:
    webhook_id: str
    event_id: str
    topic: str
    shop_domain: str
    api_version: str
    triggered_at: str
    received_at: str
    payload: dict[str, object]
    @classmethod
    def create(cls, *, webhook_id: str, event_id: str, topic: str, shop_domain: str, api_version: str, triggered_at: str, payload: dict[str, object]) -> "ShopifyWebhookEnvelope":
        return cls(webhook_id, event_id, topic, shop_domain, api_version, triggered_at, datetime.now(timezone.utc).isoformat(), payload)
    def to_dict(self) -> dict[str, object]:
        return asdict(self)
