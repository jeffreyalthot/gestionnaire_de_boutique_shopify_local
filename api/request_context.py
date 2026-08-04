from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class RequestContext:
    request_id: str
    actor: str = "api"
    client_ip: str = ""
    method: str = ""
    path: str = ""
    shop_domain: str = ""
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self) -> None:
        self.request_id = str(self.request_id).strip()
        if not self.request_id or len(self.request_id) > 128:
            raise ValueError("request_id_invalid")
        self.actor = str(self.actor or "api")[:128]
        self.client_ip = str(self.client_ip)[:64]
        self.method = str(self.method).upper()[:16]
        self.path = str(self.path)[:1024]
        self.shop_domain = str(self.shop_domain).lower()[:253]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
