from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Iterable


@dataclass(slots=True)
class ShopifyCapabilities:
    granted_scopes: set[str] = field(default_factory=set)
    mutations: set[str] = field(default_factory=set)
    queries: set[str] = field(default_factory=set)
    api_version: str = ""

    def can(self, scope: str) -> bool:
        return str(scope) in self.granted_scopes

    def can_mutate(self, mutation: str, required_scopes: Iterable[str] = ()) -> bool:
        return str(mutation) in self.mutations and all(self.can(scope) for scope in required_scopes)

    def can_query(self, query: str, required_scopes: Iterable[str] = ()) -> bool:
        return (not self.queries or str(query) in self.queries) and all(self.can(scope) for scope in required_scopes)

    def update_scopes(self, scopes: Iterable[str]) -> tuple[str, ...]:
        previous = set(self.granted_scopes)
        self.granted_scopes = {str(scope).strip() for scope in scopes if str(scope).strip()}
        return tuple(sorted(previous.symmetric_difference(self.granted_scopes)))

    def snapshot(self) -> dict[str, object]:
        return {
            "granted_scopes": tuple(sorted(self.granted_scopes)),
            "mutations": tuple(sorted(self.mutations)),
            "queries": tuple(sorted(self.queries)),
            "api_version": self.api_version,
        }
