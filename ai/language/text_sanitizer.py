from __future__ import annotations

import html
import re
from collections.abc import Mapping, Sequence
from typing import Any

_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_SPACES = re.compile(r"[ \t]+")
_EMAIL = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
_PHONE = re.compile(r"(?<!\d)(?:\+?\d[\d .()\-]{7,}\d)(?!\d)")
_CARD = re.compile(r"(?<!\d)(?:\d[ -]*?){13,19}(?!\d)")
_SCRIPT_STYLE = re.compile(r"(?is)<(script|style)\b[^>]*>.*?</\1\s*>")
_TAG = re.compile(r"(?s)<[^>]+>")


def normalize_whitespace(text: str) -> str:
    rows = [_SPACES.sub(" ", row).strip() for row in str(text).splitlines()]
    return "\n".join(row for row in rows if row).strip()


def sanitize(text: str, maximum: int = 5000) -> str:
    """Remove terminal control characters and enforce a deterministic limit."""
    if maximum < 0:
        raise ValueError("maximum must be non-negative")
    cleaned = _CONTROL.sub("", str(text)).replace("\u00a0", " ")
    return normalize_whitespace(cleaned)[:maximum]


def sanitize_html(text: str, maximum: int = 20_000, *, preserve_line_breaks: bool = True) -> str:
    """Convert untrusted HTML to plain text without optional dependencies."""
    value = _SCRIPT_STYLE.sub("", str(text))
    if preserve_line_breaks:
        value = re.sub(r"(?i)<br\s*/?>|</p\s*>|</li\s*>", "\n", value)
    value = _TAG.sub("", value)
    return sanitize(html.unescape(value), maximum)


def redact_sensitive(text: str) -> str:
    value = _EMAIL.sub("[EMAIL_REDACTED]", str(text))
    value = _CARD.sub("[PAYMENT_DATA_REDACTED]", value)
    value = _PHONE.sub("[PHONE_REDACTED]", value)
    return value


def sanitize_mapping(value: Any, maximum: int = 5000, *, redact: bool = False) -> Any:
    """Recursively sanitize strings while preserving JSON-compatible structure."""
    if isinstance(value, str):
        result = sanitize(value, maximum)
        return redact_sensitive(result) if redact else result
    if isinstance(value, Mapping):
        return {
            sanitize(str(key), 200): sanitize_mapping(item, maximum, redact=redact)
            for key, item in value.items()
        }
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        return [sanitize_mapping(item, maximum, redact=redact) for item in value]
    return value
