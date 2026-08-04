from __future__ import annotations

from typing import Any, TypeVar

T = TypeVar("T")


def get_container(request: Any) -> Any:
    app = getattr(request, "app", None)
    state = getattr(app, "state", None)
    container = getattr(state, "container", None)
    if container is None:
        raise RuntimeError("application container is not initialized")
    return container


def get_service(request: Any, name: str) -> Any:
    container = get_container(request)
    registry = getattr(container, "service_registry", None)
    if registry is None:
        raise RuntimeError("service registry is unavailable")
    return registry.get(name)


def require_live_mode(request: Any) -> Any:
    container = get_container(request)
    if container.settings.app_dry_run:
        raise PermissionError("operation requires supervised live mode")
    container.lockdown.assert_allowed()
    return container
