from __future__ import annotations
from dataclasses import replace
from typing import Any
from app.exception_router import ExceptionRouter,RoutedException

class ExceptionClassifier(ExceptionRouter):
    """Classification métier avec stratégie de reprise et anonymisation du contexte."""
    SECRET_KEYS=("token","secret","password","authorization","card","cvv")
    def _redact(self,value: Any) -> Any:
        if isinstance(value,dict):return {k:("***" if any(x in k.lower() for x in self.SECRET_KEYS) else self._redact(v)) for k,v in value.items()}
        if isinstance(value,list):return [self._redact(x) for x in value[:100]]
        if isinstance(value,str) and len(value)>1000:return value[:1000]+"…"
        return value
    def classify(self,exc: BaseException,*,operation: str="",payload: dict[str,Any] | None=None) -> RoutedException:
        routed=super().classify(exc,operation=operation,payload=self._redact(payload or {}))
        lower=routed.message.lower()
        if any(x in lower for x in ("duplicate","idempot", "already exists")):return replace(routed,category="idempotency",severity="info",retryable=False)
        if any(x in lower for x in ("insufficient funds","budget exceeded","margin")):return replace(routed,category="financial_policy",severity="error",retryable=False)
        if any(x in lower for x in ("hmac","signature","replay","spoof")):return replace(routed,category="security",severity="critical",retryable=False)
        if any(x in lower for x in ("stock","inventory","oversell")):return replace(routed,category="inventory",severity="warning",retryable=True)
        return routed
    def retry_delay(self,routed: RoutedException,attempt: int,base_seconds: float=5.0) -> float | None:
        if not routed.retryable:return None
        factor=1.5 if routed.category=="inventory" else 2.0
        return min(3600.0,max(0.1,base_seconds)*(factor**max(0,min(int(attempt),10))))

__all__=["ExceptionClassifier","RoutedException"]
