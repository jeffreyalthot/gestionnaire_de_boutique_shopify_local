from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
version = (root / "VERSION").read_text(encoding="utf-8").strip()
ignored_exact = {"__pycache__", ".pytest_cache", ".git", ".venv", "venv", "dist"}

def ignored(path: Path) -> bool:
    return any(part in ignored_exact or part.startswith(("build-", "build_")) or part == "build" for part in path.parts)

files = []
for path in sorted(item for item in root.rglob("*") if item.is_file()):
    relative = path.relative_to(root)
    if ignored(relative) or path.name in {"MANIFEST.json", "SHA256SUMS.txt"}:
        continue
    data = path.read_bytes()
    files.append({"path": relative.as_posix(), "size": len(data), "sha256": hashlib.sha256(data).hexdigest()})
(root / "MANIFEST.json").write_text(json.dumps({"version": version, "file_count": len(files), "files": files}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(len(files))
