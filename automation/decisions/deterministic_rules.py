from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

Predicate = Callable[[dict[str, Any]], bool]


@dataclass(frozen=True, slots=True)
class Rule:
    name: str
    predicate: Predicate
    effect: str
    reason: str
    priority: int = 100


class DeterministicRules:
    def __init__(self) -> None:
        self._rules: list[Rule] = []

    def add(self, rule: Rule) -> None:
        if rule.effect not in {"allow", "deny", "hold", "flag"}:
            raise ValueError("Effet de règle invalide.")
        self._rules.append(rule)
        self._rules.sort(key=lambda item: (item.priority, item.name))

    def evaluate(self, facts: dict[str, Any]) -> tuple[dict[str, str], ...]:
        matches: list[dict[str, str]] = []
        for rule in self._rules:
            try:
                matched = bool(rule.predicate(facts))
            except Exception:
                matched = False
            if matched:
                matches.append({"rule": rule.name, "effect": rule.effect, "reason": rule.reason})
        return tuple(matches)
