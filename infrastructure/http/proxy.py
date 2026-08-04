from __future__ import annotations

from dataclasses import asdict, dataclass
from ipaddress import ip_address
from urllib.parse import urlsplit, urlunsplit


@dataclass(frozen=True, slots=True)
class ProxyConfiguration:
    url: str
    scheme: str
    host: str
    port: int
    authenticated: bool
    safe_for_logs: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def parse_proxy(url: str, *, allow_http: bool = True, allow_local: bool = False) -> ProxyConfiguration | None:
    value = str(url or "").strip()
    if not value:
        return None
    parsed = urlsplit(value)
    if parsed.scheme not in ({"http", "https"} if allow_http else {"https"}):
        raise ValueError("Schéma de proxy non autorisé")
    if not parsed.hostname:
        raise ValueError("Hôte du proxy requis")
    host = parsed.hostname.casefold()
    try:
        address = ip_address(host)
        if not allow_local and (address.is_loopback or address.is_private or address.is_link_local):
            raise ValueError("Proxy local ou privé interdit")
    except ValueError as exc:
        if "interdit" in str(exc):
            raise
        if not allow_local and host in {"localhost", "localhost.localdomain"}:
            raise ValueError("Proxy local interdit")
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    safe_netloc = host + (f":{port}" if port else "")
    return ProxyConfiguration(
        url=value,
        scheme=parsed.scheme,
        host=host,
        port=port,
        authenticated=bool(parsed.username or parsed.password),
        safe_for_logs=urlunsplit((parsed.scheme, safe_netloc, parsed.path, "", "")),
    )


def normalize_proxy(url: str) -> str | None:
    config = parse_proxy(url, allow_local=True)
    return config.url if config else None
