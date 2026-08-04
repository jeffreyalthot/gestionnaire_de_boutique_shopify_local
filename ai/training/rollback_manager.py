from __future__ import annotations

import hashlib
import os
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True, slots=True)
class RollbackResult:
    source: str
    destination: str
    sha256: str
    byte_size: int
    completed_at: str

    @property
    def restored(self) -> bool:
        return bool(self.destination and self.sha256)

    def as_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["restored"] = self.restored
        return data


class RollbackManager:
    def rollback(self, rollback_path: Path, active_path: Path) -> RollbackResult:
        rollback_path = Path(rollback_path)
        active_path = Path(active_path)
        if not rollback_path.is_file():
            raise FileNotFoundError(rollback_path)
        active_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = active_path.with_suffix(active_path.suffix + ".rollback.tmp")
        shutil.copy2(rollback_path, temporary)
        data = temporary.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        os.replace(temporary, active_path)
        return RollbackResult(
            source=str(rollback_path), destination=str(active_path), sha256=digest,
            byte_size=len(data), completed_at=datetime.now(timezone.utc).isoformat(),
        )


def rollback_model(rollback_path: Path, active_path: Path) -> None:
    RollbackManager().rollback(rollback_path, active_path)
