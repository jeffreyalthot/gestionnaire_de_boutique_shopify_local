from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import AsyncIterator

import httpx

from catalog.media.media_url_validator import MediaURLValidator


@dataclass(frozen=True, slots=True)
class DownloadedAsset:
    url: str
    content_type: str
    byte_size: int
    sha256: str
    path: Path


class ImageDownloader:
    ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

    def __init__(self, cache_directory: Path, *, max_bytes: int = 12 * 1024 * 1024,
                 validator: MediaURLValidator | None = None, timeout: float = 20.0) -> None:
        self.cache_directory = Path(cache_directory)
        self.cache_directory.mkdir(parents=True, exist_ok=True)
        self.max_bytes = max_bytes
        self.validator = validator or MediaURLValidator()
        self.timeout = timeout

    async def download(self, url: str, client: httpx.AsyncClient | None = None) -> DownloadedAsset:
        validation = self.validator.validate(url, resolve_dns=False)
        if not validation.allowed:
            raise ValueError(f"URL média refusée: {validation.reason}")
        owns = client is None
        client = client or httpx.AsyncClient(timeout=self.timeout, follow_redirects=False)
        temp = self.cache_directory / ".partial-download"
        digest = sha256()
        size = 0
        content_type = ""
        try:
            async with client.stream("GET", url, headers={"Accept": "image/*"}) as response:
                response.raise_for_status()
                content_type = response.headers.get("content-type", "").split(";", 1)[0].lower()
                if content_type not in self.ALLOWED_TYPES:
                    raise ValueError(f"Type média refusé: {content_type}")
                declared = int(response.headers.get("content-length", "0") or 0)
                if declared > self.max_bytes:
                    raise ValueError("Média trop volumineux")
                with temp.open("wb") as handle:
                    async for chunk in response.aiter_bytes(65536):
                        size += len(chunk)
                        if size > self.max_bytes:
                            raise ValueError("Média trop volumineux")
                        digest.update(chunk)
                        handle.write(chunk)
            suffix = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/gif": ".gif"}[content_type]
            target = self.cache_directory / f"{digest.hexdigest()}{suffix}"
            temp.replace(target)
            return DownloadedAsset(url, content_type, size, digest.hexdigest(), target)
        finally:
            temp.unlink(missing_ok=True)
            if owns:
                await client.aclose()
