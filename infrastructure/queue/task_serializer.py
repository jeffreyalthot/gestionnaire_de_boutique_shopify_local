from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from infrastructure.queue.task import QueueTask


class TaskSerializationError(ValueError):
    pass


def serialize_task(task: QueueTask, *, maximum_bytes: int = 1_000_000) -> str:
    body = json.dumps(task.as_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    if len(body.encode("utf-8")) > maximum_bytes:
        raise TaskSerializationError("queue_task_too_large")
    return body


def deserialize_task(value: str | bytes, *, maximum_bytes: int = 1_000_000) -> QueueTask:
    raw = value.encode("utf-8") if isinstance(value, str) else bytes(value)
    if len(raw) > maximum_bytes:
        raise TaskSerializationError("queue_task_too_large")
    try:
        payload = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TaskSerializationError("queue_task_json_invalid") from exc
    if not isinstance(payload, Mapping):
        raise TaskSerializationError("queue_task_object_required")
    try:
        return QueueTask.from_mapping(payload)
    except (TypeError, ValueError) as exc:
        raise TaskSerializationError(str(exc)) from exc


def task_fingerprint(task: QueueTask) -> str:
    return hashlib.sha256(serialize_task(task).encode("utf-8")).hexdigest()
