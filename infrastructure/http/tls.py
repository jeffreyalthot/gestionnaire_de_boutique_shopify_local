from __future__ import annotations

import ssl
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TLSPolicy:
    minimum_version: ssl.TLSVersion = ssl.TLSVersion.TLSv1_2
    check_hostname: bool = True
    verify_mode: ssl.VerifyMode = ssl.CERT_REQUIRED
    ca_file: str | None = None

    def context(self) -> ssl.SSLContext:
        context = ssl.create_default_context(cafile=self.ca_file)
        context.minimum_version = self.minimum_version
        context.check_hostname = self.check_hostname
        context.verify_mode = self.verify_mode
        if hasattr(ssl, "OP_NO_COMPRESSION"):
            context.options |= ssl.OP_NO_COMPRESSION
        return context


def secure_ssl_context() -> ssl.SSLContext:
    return TLSPolicy().context()
