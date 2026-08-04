from __future__ import annotations

import ipaddress
import socket
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True, slots=True)
class URLValidation:
    allowed: bool
    reason: str
    host: str = ""


class MediaURLValidator:
    def __init__(self, allowed_hosts: set[str] | None = None) -> None:
        self.allowed_hosts = {host.lower() for host in (allowed_hosts or set())}

    def validate(self, url: str, *, resolve_dns: bool = False) -> URLValidation:
        try:
            parsed = urlparse(url)
        except ValueError:
            return URLValidation(False, "invalid_url")
        if parsed.scheme not in {"https", "http"}:
            return URLValidation(False, "unsupported_scheme")
        if parsed.username or parsed.password:
            return URLValidation(False, "credentials_forbidden")
        host = (parsed.hostname or "").lower().rstrip(".")
        if not host:
            return URLValidation(False, "missing_host")
        if self.allowed_hosts and host not in self.allowed_hosts and not any(host.endswith("." + item) for item in self.allowed_hosts):
            return URLValidation(False, "host_not_allowlisted", host)
        try:
            ip = ipaddress.ip_address(host)
            if not ip.is_global:
                return URLValidation(False, "non_public_ip", host)
        except ValueError:
            if host in {"localhost", "localhost.localdomain"} or host.endswith(".local"):
                return URLValidation(False, "local_host", host)
            if resolve_dns:
                try:
                    for info in socket.getaddrinfo(host, parsed.port or 443, type=socket.SOCK_STREAM):
                        ip = ipaddress.ip_address(info[4][0])
                        if not ip.is_global:
                            return URLValidation(False, "dns_resolves_private", host)
                except OSError:
                    return URLValidation(False, "dns_failure", host)
        return URLValidation(True, "allowed", host)
