from __future__ import annotations

import asyncio
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import Any

Subscriber = Callable[[dict[str, Any]], Awaitable[None]]


class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Subscriber]] = defaultdict(list)

    def subscribe(self, topic: str, subscriber: Subscriber) -> None:
        self._subscribers[topic].append(subscriber)

    async def publish(self, topic: str, event: dict[str, Any]) -> list[Exception]:
        results = await asyncio.gather(*(subscriber(event) for subscriber in self._subscribers.get(topic, ())), return_exceptions=True)
        return [result for result in results if isinstance(result, Exception)]
