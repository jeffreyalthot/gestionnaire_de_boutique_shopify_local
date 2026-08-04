from __future__ import annotations

from catalog.media.content_type_detector import detect_content_type


class MediaContentGuard:
    ALLOWED={"image/jpeg","image/png","image/webp","image/gif"}
    def inspect(self, data: bytes, declared_type: str, maximum_bytes: int = 12*1024*1024) -> dict[str, object]:
        if len(data)>maximum_bytes: return {"allowed":False,"reason":"too_large"}
        detected=detect_content_type(data)
        if detected not in self.ALLOWED: return {"allowed":False,"reason":"unsupported_content","detected":detected}
        if declared_type.split(';',1)[0].lower()!=detected: return {"allowed":False,"reason":"mime_mismatch","detected":detected}
        return {"allowed":True,"reason":"allowed","detected":detected}
