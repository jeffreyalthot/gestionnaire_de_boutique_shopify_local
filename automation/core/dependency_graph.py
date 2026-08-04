from __future__ import annotations

from collections import defaultdict, deque
from typing import Iterable


class DependencyGraph:
    def __init__(self) -> None:
        self._dependencies: dict[str, set[str]] = defaultdict(set)

    def add(self, node: str, depends_on: Iterable[str] = ()) -> None:
        key = node.strip()
        if not key:
            raise ValueError("Le nœud est requis.")
        self._dependencies[key].update(item.strip() for item in depends_on if item.strip())
        for dependency in self._dependencies[key]:
            self._dependencies.setdefault(dependency, set())

    def order(self, selected: Iterable[str] | None = None) -> tuple[str, ...]:
        nodes = set(selected or self._dependencies)
        expanded = set(nodes)
        queue = deque(nodes)
        while queue:
            node = queue.popleft()
            for dep in self._dependencies.get(node, ()):
                if dep not in expanded:
                    expanded.add(dep)
                    queue.append(dep)
        indegree = {node: 0 for node in expanded}
        reverse: dict[str, set[str]] = defaultdict(set)
        for node in expanded:
            for dep in self._dependencies.get(node, ()):
                if dep in expanded:
                    indegree[node] += 1
                    reverse[dep].add(node)
        ready = deque(sorted(node for node, degree in indegree.items() if degree == 0))
        result: list[str] = []
        while ready:
            node = ready.popleft()
            result.append(node)
            for follower in sorted(reverse[node]):
                indegree[follower] -= 1
                if indegree[follower] == 0:
                    ready.append(follower)
        if len(result) != len(expanded):
            cycle = tuple(sorted(node for node, degree in indegree.items() if degree > 0))
            raise ValueError(f"Cycle de dépendances: {cycle}")
        return tuple(result)

    def snapshot(self) -> dict[str, tuple[str, ...]]:
        return {node: tuple(sorted(deps)) for node, deps in sorted(self._dependencies.items())}
