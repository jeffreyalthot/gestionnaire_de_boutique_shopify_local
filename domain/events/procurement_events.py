from __future__ import annotations

from typing import Any, Mapping

from domain.events.base_event import DomainEvent


def procurement_event(action: str, payload: dict[str, object], **metadata: Any) -> DomainEvent:
    return DomainEvent.create("procurement", action, payload, **metadata)


def create(action: str, payload: Mapping[str, Any], **metadata: Any) -> DomainEvent:
    return DomainEvent.create("procurement", action, payload, **metadata)
