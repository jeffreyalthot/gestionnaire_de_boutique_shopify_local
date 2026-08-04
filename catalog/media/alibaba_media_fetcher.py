from __future__ import annotations

from pathlib import Path
from typing import Any

from catalog.media.image_downloader import ImageDownloader
from catalog.media.media_rights_guard import MediaRightsGuard
from catalog.media.media_url_validator import MediaUrlValidator


class AlibabaMediaFetcher:
    def __init__(self, *, downloader: ImageDownloader, validator: MediaUrlValidator | None = None,
                 rights: MediaRightsGuard | None = None) -> None:
        self.downloader = downloader
        self.validator = validator or MediaUrlValidator()
        self.rights = rights or MediaRightsGuard()

    async def fetch(self, url: str, destination: Path, metadata: dict[str, Any]) -> dict[str, Any]:
        self.validator.validate(url)
        decision = self.rights.evaluate(metadata)
        if not decision.allowed:
            return {"status": "blocked", "reason": decision.reason, "rights_status": decision.status}
        result = await self.downloader.download(url, destination)
        return {"status": "downloaded", "rights_status": decision.status, **result}
