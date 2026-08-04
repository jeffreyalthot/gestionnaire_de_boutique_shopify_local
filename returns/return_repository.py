from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from threading import RLock
from typing import Iterable

from returns.return_request import ReturnRequest


class ReturnRepository:
    VALID_TRANSITIONS = {
        "requested": {"approved", "rejected", "cancelled"},
        "approved": {"label_created", "in_transit", "refunded", "cancelled"},
        "label_created": {"in_transit", "cancelled"},
        "in_transit": {"received", "lost"},
        "received": {"inspected", "refunded", "rejected"},
        "inspected": {"refunded", "exchanged", "rejected"},
        "lost": {"refunded", "closed"},
        "refunded": {"closed"},
        "exchanged": {"closed"},
        "rejected": {"closed"},
        "cancelled": set(),
        "closed": set(),
    }

    def __init__(self) -> None:
        self._items: dict[str, ReturnRequest] = {}
        self._history: dict[str, list[dict[str, object]]] = {}
        self._lock = RLock()

    def save(self, request: ReturnRequest) -> None:
        with self._lock:
            existing = self._items.get(request.id)
            if existing and existing.order_id != request.order_id:
                raise ValueError("Un retour ne peut pas changer de commande")
            self._items[request.id] = request
            self._history.setdefault(request.id, []).append({
                "status": request.status,
                "at": datetime.now(timezone.utc).isoformat(),
                "reason": "saved",
            })

    def get(self, return_id: str) -> ReturnRequest | None:
        with self._lock:
            return self._items.get(return_id)

    def list(self, status: str | None = None) -> tuple[ReturnRequest, ...]:
        with self._lock:
            return tuple(item for item in self._items.values() if status is None or item.status == status)

    def transition(self, return_id: str, target: str, *, reason: str = "", force: bool = False) -> ReturnRequest:
        with self._lock:
            current = self._items.get(return_id)
            if current is None:
                raise KeyError(return_id)
            target_status = str(target).strip().lower()
            allowed = self.VALID_TRANSITIONS.get(current.status, set())
            if not force and target_status not in allowed:
                raise ValueError(f"Transition invalide: {current.status} -> {target_status}")
            updated = replace(current, status=target_status)
            self._items[return_id] = updated
            self._history.setdefault(return_id, []).append({
                "status": target_status,
                "at": datetime.now(timezone.utc).isoformat(),
                "reason": str(reason),
            })
            return updated

    def history(self, return_id: str) -> tuple[dict[str, object], ...]:
        with self._lock:
            return tuple(dict(item) for item in self._history.get(return_id, ()))

    def by_order(self, order_id: str) -> tuple[ReturnRequest, ...]:
        with self._lock:
            return tuple(item for item in self._items.values() if item.order_id == order_id)
