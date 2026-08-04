from __future__ import annotations

from dataclasses import asdict, dataclass
from urllib.parse import urlparse


@dataclass(frozen=True, slots=True)
class TmcEndpoint:
    url: str
    production: bool
    secure: bool
    host: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class TmcWebsocketAdapter:
    production_url = "ws://mc.api.taobao.com/"
    preproduction_url = "ws://premc.api.taobao.com/"

    def endpoint(self, production: bool = True, *, require_tls: bool = False) -> str:
        url = self.production_url if production else self.preproduction_url
        parsed = urlparse(url)
        if parsed.scheme not in {"ws", "wss"} or not parsed.hostname:
            raise ValueError("Endpoint TMC invalide.")
        if require_tls and parsed.scheme != "wss":
            raise ValueError("TLS WebSocket requis pour TMC.")
        return url

    def describe(self, production: bool = True) -> TmcEndpoint:
        url = self.endpoint(production)
        parsed = urlparse(url)
        return TmcEndpoint(url, bool(production), parsed.scheme == "wss", parsed.hostname or "")
