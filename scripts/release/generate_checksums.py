from __future__ import annotations
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
ignored_exact = {"__pycache__", ".pytest_cache", ".git", ".venv", "venv", "dist"}

def ignored(path: Path) -> bool:
    return any(part in ignored_exact or part.startswith(("build-", "build_")) or part == "build" for part in path.parts)

rows = []
for path in sorted(item for item in root.rglob("*") if item.is_file()):
    relative = path.relative_to(root)
    if ignored(relative) or path.name == "SHA256SUMS.txt":
        continue
    rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {relative.as_posix()}")
(root / "SHA256SUMS.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows))
