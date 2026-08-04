from __future__ import annotations
from abc import ABC,abstractmethod
from dataclasses import dataclass
@dataclass(frozen=True)
class SearchSignal:
    term: str; score: float; source: str; detail: dict
class SearchProvider(ABC):
    @abstractmethod
    async def signals(self,terms: list[str])->list[SearchSignal]:...
