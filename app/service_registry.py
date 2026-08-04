from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ServiceDescriptor:
    name: str
    instance: Any
    critical: bool = False
    tags: tuple[str, ...] = ()


class ServiceRegistry:
    """Registre explicite évitant les singletons implicites et les dépendances cachées."""

    def __init__(self) -> None:
        self._services: dict[str, ServiceDescriptor] = {}

    def register(self, name: str, instance: Any, *, critical: bool = False, tags: tuple[str, ...] = ()) -> None:
        key = name.strip().lower()
        if not key:
            raise ValueError("Le nom du service est requis.")
        if key in self._services:
            raise ValueError(f"Service déjà enregistré: {key}")
        self._services[key] = ServiceDescriptor(key, instance, critical, tuple(sorted(set(tags))))

    def get(self, name: str, expected_type: type[Any] | None = None) -> Any:
        key = name.strip().lower()
        if key not in self._services:
            raise KeyError(f"Service absent: {key}")
        instance = self._services[key].instance
        if expected_type is not None and not isinstance(instance, expected_type):
            raise TypeError(f"{key} n'est pas de type {expected_type.__name__}")
        return instance

    def descriptors(self) -> tuple[ServiceDescriptor, ...]:
        return tuple(self._services[key] for key in sorted(self._services))

    def snapshot(self) -> dict[str, Any]:
        return {
            item.name: {"critical": item.critical, "tags": item.tags, "type": type(item.instance).__name__}
            for item in self.descriptors()
        }
