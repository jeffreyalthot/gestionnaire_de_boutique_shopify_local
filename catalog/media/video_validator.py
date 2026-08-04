from __future__ import annotations


class VideoValidator:
    ALLOWED = {"video/mp4", "video/webm"}

    def validate(self, *, content_type: str, byte_size: int, duration_seconds: float,
                 width: int, height: int) -> dict[str, object]:
        issues: list[str] = []
        if content_type not in self.ALLOWED: issues.append("unsupported_type")
        if byte_size <= 0 or byte_size > 1024 * 1024 * 1024: issues.append("invalid_size")
        if duration_seconds <= 0 or duration_seconds > 600: issues.append("invalid_duration")
        if width < 480 or height < 270: issues.append("low_resolution")
        return {"valid": not issues, "issues": tuple(issues)}
