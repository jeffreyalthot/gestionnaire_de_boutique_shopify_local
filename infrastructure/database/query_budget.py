from __future__ import annotations
import time
from contextlib import contextmanager

class QueryBudgetExceeded(RuntimeError): pass
class QueryBudget:
    def __init__(self,max_queries: int=100,max_seconds: float=5.0)->None:
        self.max_queries=max_queries; self.max_seconds=max_seconds; self.queries=0; self.started=time.monotonic()
    def consume(self,count: int=1)->None:
        self.queries+=count
        if self.queries>self.max_queries or time.monotonic()-self.started>self.max_seconds: raise QueryBudgetExceeded('Budget de requêtes dépassé.')
    @contextmanager
    def query(self): self.consume(); yield
