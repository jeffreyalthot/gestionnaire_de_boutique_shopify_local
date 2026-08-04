from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass
from uuid import uuid4

_current=ContextVar("trace_context",default=None)

@dataclass(frozen=True, slots=True)
class TraceContext:
    trace_id: str
    span_id: str
    parent_span_id: str=""

    @classmethod
    def new(cls) -> "TraceContext": return cls(str(uuid4()),str(uuid4()))
    def child(self) -> "TraceContext": return TraceContext(self.trace_id,str(uuid4()),self.span_id)
    def activate(self): return _current.set(self)
    @staticmethod
    def current(): return _current.get()
