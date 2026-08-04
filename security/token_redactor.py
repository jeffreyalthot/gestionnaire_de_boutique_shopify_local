import re
_PATTERNS = [
    re.compile(r"(?i)(access_token|refresh_token|secret|authorization)=([^&\s]+)"),
    re.compile(r"(?i)(bearer)\s+[A-Za-z0-9._~+\-/]+=*"),
]
def redact_text(value: str) -> str:
    result = value
    for pattern in _PATTERNS:
        result = pattern.sub(lambda m: f"{m.group(1)}=***" if m.lastindex and m.lastindex > 1 else "Bearer ***", result)
    return result
