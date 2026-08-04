from __future__ import annotations

from pathlib import Path
from hashlib import sha256


class RuntimeIntegrityMonitor:
    def checksum(self, path: Path) -> str:
        digest=sha256()
        with path.open('rb') as handle:
            for chunk in iter(lambda:handle.read(1024*1024),b''): digest.update(chunk)
        return digest.hexdigest()
    def verify(self, entries: dict[Path,str]) -> dict[str, object]:
        failures=[]
        for path,expected in entries.items():
            if not path.is_file(): failures.append({"path":str(path),"reason":"missing"})
            elif self.checksum(path)!=expected: failures.append({"path":str(path),"reason":"checksum"})
        return {"ok":not failures,"failures":failures,"checked":len(entries)}
