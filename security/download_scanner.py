from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScanResult:
    safe: bool
    sha256: str
    reason: str


class DownloadScanner:
    MAGIC={b"\x89PNG\r\n\x1a\n":"image/png",b"\xff\xd8\xff":"image/jpeg",b"RIFF":"image/webp"}
    def scan(self, data: bytes, *, claimed_type: str, max_bytes: int=12_582_912) -> ScanResult:
        digest=hashlib.sha256(data).hexdigest()
        if not data: return ScanResult(False,digest,"empty")
        if len(data)>max_bytes: return ScanResult(False,digest,"too_large")
        detected=next((mime for magic,mime in self.MAGIC.items() if data.startswith(magic)),"unknown")
        if detected=="unknown": return ScanResult(False,digest,"unsupported_signature")
        if claimed_type and claimed_type.split(";",1)[0].lower()!=detected: return ScanResult(False,digest,"content_type_mismatch")
        return ScanResult(True,digest,detected)
