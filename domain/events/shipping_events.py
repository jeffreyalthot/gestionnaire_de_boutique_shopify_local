from __future__ import annotations

from typing import Any, Mapping

from domain.events.base_event import DomainEvent


def shipping_event(action: str, payload: dict[str, object], **metadata: Any) -> DomainEvent:
    return DomainEvent.create("shipping", action, payload, **metadata)


def create(action: str, payload: Mapping[str, Any], **metadata: Any) -> DomainEvent:
    return DomainEvent.create("shipping", action, payload, **metadata)
