from __future__ import annotations

MAGIC: tuple[tuple[bytes, str], ...] = (
    (b"\xff\xd8\xff", "image/jpeg"),
    (b"\x89PNG\r\n\x1a\n", "image/png"),
    (b"GIF87a", "image/gif"),
    (b"GIF89a", "image/gif"),
    (b"RIFF", "image/webp"),
)


def detect_content_type(data: bytes) -> str:
    for prefix, content_type in MAGIC:
        if data.startswith(prefix):
            if content_type == "image/webp" and data[8:12] != b"WEBP":
                continue
            return content_type
    return "application/octet-stream"
