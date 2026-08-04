from __future__ import annotations

import re
from pathlib import Path

_STATIC_PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"),
    "shopify_token": re.compile(r"shpat_[A-Za-z0-9]{20,}"),
}
_CARD_CANDIDATE = re.compile(r"(?<!\d)(?:\d[ -]*?){13,19}(?!\d)")
_IGNORED_DIRECTORIES = {
    ".git", ".pytest_cache", ".mypy_cache", ".ruff_cache", "__pycache__",
    "build", "dist", ".venv", "venv", "node_modules", "model_files",
}
_IGNORED_SUFFIXES = {
    ".db", ".db-wal", ".db-shm", ".zip", ".tar", ".gz", ".7z",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf",
    ".exe", ".dll", ".so", ".dylib", ".a", ".lib", ".o", ".obj",
    ".pyc", ".pyd", ".woff", ".woff2", ".ttf",
}
_MAX_TEXT_BYTES = 2 * 1024 * 1024


def _luhn_valid(candidate: str) -> bool:
    digits = [int(ch) for ch in candidate if ch.isdigit()]
    if not 13 <= len(digits) <= 19 or len(set(digits)) == 1:
        return False
    checksum = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


def scan_text(text: str) -> list[str]:
    findings = [name for name, pattern in _STATIC_PATTERNS.items() if pattern.search(text)]
    if any(_luhn_valid(match.group(0)) for match in _CARD_CANDIDATE.finditer(text)):
        findings.append("credit_card")
    return findings


def _eligible(path: Path, root: Path) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return False
    if any(part in _IGNORED_DIRECTORIES or part.startswith(("build-", "build_", "dist-", "dist_")) for part in relative.parts[:-1]):
        return False
    if path.name in {"MANIFEST.json", "SHA256SUMS.txt"}:
        return False
    suffixes = "".join(path.suffixes[-2:]).lower()
    if path.suffix.lower() in _IGNORED_SUFFIXES or suffixes in _IGNORED_SUFFIXES:
        return False
    try:
        return path.stat().st_size <= _MAX_TEXT_BYTES
    except OSError:
        return False


def scan_tree(root: Path) -> list[tuple[str, str]]:
    root = root.resolve()
    findings: list[tuple[str, str]] = []
    for path in root.rglob("*"):
        if not path.is_file() or not _eligible(path, root):
            continue
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if b"\x00" in data[:4096]:
            continue
        text = data.decode("utf-8", errors="ignore")
        for name in scan_text(text):
            findings.append((str(path), name))
    return findings
