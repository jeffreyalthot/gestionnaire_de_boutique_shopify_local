from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from urllib.parse import urlparse

from catalog.image_validator import valid_image_urls


@dataclass(frozen=True, slots=True)
class PreparedImage:
    original_source: str
    alt: str
    content_type: str
    source_host: str
    fingerprint: str
    position: int

    def as_shopify_file(self) -> dict[str, str]:
        return {
            "originalSource": self.original_source,
            "alt": self.alt,
            "contentType": self.content_type,
        }

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ImagePipeline:
    def prepare(self, urls: list[str], title: str, *, maximum: int = 20) -> tuple[PreparedImage, ...]:
        clean_urls = valid_image_urls(urls)[: max(1, int(maximum))]
        seen: set[str] = set()
        images: list[PreparedImage] = []
        for index, url in enumerate(clean_urls):
            fingerprint = sha256(url.encode("utf-8")).hexdigest()
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            images.append(PreparedImage(
                original_source=url,
                alt=f"{title} — image {len(images) + 1}",
                content_type="IMAGE",
                source_host=(urlparse(url).hostname or "").lower(),
                fingerprint=fingerprint,
                position=len(images),
            ))
        return tuple(images)

    def shopify_files(self, urls: list[str], title: str, *, maximum: int = 20) -> list[dict[str, str]]:
        return [item.as_shopify_file() for item in self.prepare(urls, title, maximum=maximum)]


def shopify_files(urls: list[str], title: str) -> list[dict[str, str]]:
    return ImagePipeline().shopify_files(urls, title)
