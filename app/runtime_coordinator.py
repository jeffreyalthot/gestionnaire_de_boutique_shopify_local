from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.runtime_snapshot import RuntimeSnapshot


class RuntimeCoordinator:
    """Coordonne snapshot, santé, récupération et cycle sans thread supplémentaire."""

    def __init__(self, container: Any, health: Any, recovery: Any) -> None:
        self.container = container
        self.health = health
        self.recovery = recovery
        self._lock = asyncio.Lock()
        self._last_snapshot: RuntimeSnapshot | None = None

    async def snapshot(self, *, persist: bool = True) -> RuntimeSnapshot:
        async with self._lock:
            state = self.container.dashboard_state()
            health = await self.health.collect()
            snapshot = RuntimeSnapshot(
                id=str(uuid4()),
                created_at=datetime.now(timezone.utc).isoformat(),
                status=str(health["status"]),
                phase=str(state.get("automation", {}).get("phase", "idle")),
                resource=dict(state.get("runtime", {}).get("resource", {})),
                queue={str(k): int(v) for k, v in dict(state.get("queue", {})).items()},
                automation=dict(state.get("automation", {})),
                integrations=dict(state.get("api", {})),
                health=health,
            )
            if persist:
                self.container.db.execute(
                    "INSERT INTO runtime_snapshots(id,snapshot_json,created_at) VALUES(?,?,?)",
                    (snapshot.id, json.dumps(snapshot.as_dict(), ensure_ascii=False, default=str), snapshot.created_at),
                )
            self._last_snapshot = snapshot
            return snapshot

    def recover(self) -> dict[str, Any]:
        return self.recovery.recover().as_dict()

    def last_snapshot(self) -> dict[str, Any] | None:
        return self._last_snapshot.as_dict() if self._last_snapshot else None
