from __future__ import annotations

import hashlib
import json
from collections import deque
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from threading import RLock
from typing import Any, Callable, Iterable, Mapping


Guard = Callable[[Mapping[str, Any]], bool]


@dataclass(frozen=True, slots=True)
class Transition:
    source: str
    target: str
    event: str
    guard: Guard | None = None
    reason: str = ""
    reversible: bool = True


@dataclass(frozen=True, slots=True)
class TransitionResult:
    source: str
    target: str
    event: str
    changed: bool
    occurred_at: str
    reason: str
    fingerprint: str
    context: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class StateMachine:
    """Machine d'état déterministe avec gardes, introspection et audit borné."""

    def __init__(
        self,
        transitions: Iterable[Transition],
        *,
        terminal_states: Iterable[str] = (),
        history_size: int = 500,
    ) -> None:
        transition_list = tuple(transitions)
        if not transition_list:
            raise ValueError("state_machine_requires_transitions")
        self._by_key: dict[tuple[str, str], Transition] = {}
        self._states: set[str] = set()
        for transition in transition_list:
            source = str(transition.source).strip()
            target = str(transition.target).strip()
            event = str(transition.event).strip()
            if not source or not target or not event:
                raise ValueError("state_transition_invalid")
            key = (source, event)
            if key in self._by_key:
                raise ValueError(f"duplicate_transition:{source}:{event}")
            normalized = Transition(source, target, event, transition.guard, transition.reason, transition.reversible)
            self._by_key[key] = normalized
            self._states.update((source, target))
        self.terminal_states = frozenset(str(item).strip() for item in terminal_states if str(item).strip())
        unknown_terminal = self.terminal_states - self._states
        if unknown_terminal:
            raise ValueError("unknown_terminal_states:" + ",".join(sorted(unknown_terminal)))
        self._history: deque[TransitionResult] = deque(maxlen=max(1, int(history_size)))
        self._lock = RLock()

    @property
    def states(self) -> tuple[str, ...]:
        return tuple(sorted(self._states))

    def transition(self, current: str, event: str, context: Mapping[str, Any] | None = None) -> str:
        return self.apply(current, event, context).target

    def apply(self, current: str, event: str, context: Mapping[str, Any] | None = None) -> TransitionResult:
        source = str(current).strip()
        event_name = str(event).strip()
        selected = self._by_key.get((source, event_name))
        if selected is None:
            raise ValueError(f"Transition interdite: {source} + {event_name}")
        context_value = dict(context or {})
        if selected.guard is not None and not bool(selected.guard(context_value)):
            raise PermissionError(f"Transition gardée: {source} + {event_name}")
        occurred_at = datetime.now(timezone.utc).isoformat()
        material = json.dumps(
            {"source": source, "target": selected.target, "event": event_name, "context": context_value, "occurred_at": occurred_at},
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )
        result = TransitionResult(
            source,
            selected.target,
            event_name,
            source != selected.target,
            occurred_at,
            selected.reason or event_name,
            hashlib.sha256(material.encode("utf-8")).hexdigest()[:24],
            context_value,
        )
        with self._lock:
            self._history.append(result)
        return result

    def can(self, current: str, event: str, context: Mapping[str, Any] | None = None) -> bool:
        selected = self._by_key.get((str(current).strip(), str(event).strip()))
        if selected is None:
            return False
        return selected.guard is None or bool(selected.guard(dict(context or {})))

    def events(self, current: str, context: Mapping[str, Any] | None = None) -> tuple[str, ...]:
        return tuple(sorted(event for (source, event), _transition in self._by_key.items() if source == current and self.can(current, event, context)))

    def is_terminal(self, state: str) -> bool:
        return str(state) in self.terminal_states or not any(source == state for source, _event in self._by_key)

    def path(self, source: str, target: str, *, maximum_steps: int = 32) -> tuple[str, ...]:
        if source == target:
            return ()
        queue: deque[tuple[str, tuple[str, ...]]] = deque([(source, ())])
        visited = {source}
        while queue:
            state, events = queue.popleft()
            if len(events) >= maximum_steps:
                continue
            for (candidate_source, event), transition in self._by_key.items():
                if candidate_source != state:
                    continue
                if transition.target == target:
                    return (*events, event)
                if transition.target not in visited:
                    visited.add(transition.target)
                    queue.append((transition.target, (*events, event)))
        return ()

    def recent(self, limit: int = 20) -> tuple[TransitionResult, ...]:
        with self._lock:
            return tuple(list(self._history)[-max(1, int(limit)):])

    def describe(self) -> dict[str, Any]:
        return {
            "states": self.states,
            "terminal_states": tuple(sorted(self.terminal_states)),
            "transitions": tuple(
                {
                    "source": transition.source,
                    "target": transition.target,
                    "event": transition.event,
                    "guarded": transition.guard is not None,
                    "reversible": transition.reversible,
                }
                for transition in sorted(self._by_key.values(), key=lambda item: (item.source, item.event))
            ),
        }
