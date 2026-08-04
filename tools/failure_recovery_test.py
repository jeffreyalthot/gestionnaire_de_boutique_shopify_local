from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path as _BootstrapPath
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[1]))

from tools.runtime_tool import database, emit
from app.recovery_manager import RecoveryManager
from infrastructure.queue.durable_queue import DurableQueue


def main() -> int:
    _, db = database()
    queue = DurableQueue(db)
    report = RecoveryManager(db, queue).recover()
    return emit(report.as_dict())


if __name__ == "__main__":
    raise SystemExit(main())
