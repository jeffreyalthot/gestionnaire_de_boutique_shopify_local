from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class NativeDashboardBridge:
    """Échange borné par fichiers atomiques avec le terminal C++ local."""

    def __init__(self, directory: Path) -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.snapshot_path = self.directory / 'dashboard_snapshot.json'

    def publish(self, snapshot: dict[str, Any]) -> Path:
        temporary = self.snapshot_path.with_suffix('.tmp')
        temporary.write_text(json.dumps(snapshot, ensure_ascii=True, separators=(',', ':')), encoding='utf-8')
        temporary.replace(self.snapshot_path)
        return self.snapshot_path

    def read_commands(self, limit: int = 32) -> list[dict[str, Any]]:
        commands: list[dict[str, Any]] = []
        for path in sorted(self.directory.glob('command-*.json'))[:limit]:
            try:
                commands.append(json.loads(path.read_text(encoding='utf-8')))
                path.rename(path.with_suffix('.processed'))
            except (OSError, ValueError):
                path.rename(path.with_suffix('.failed'))
        return commands
