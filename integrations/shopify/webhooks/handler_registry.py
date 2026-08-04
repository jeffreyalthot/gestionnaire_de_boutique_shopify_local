from __future__ import annotations
import importlib, pkgutil
from dataclasses import dataclass
from typing import Any, Callable
import integrations.shopify.webhooks.handlers as handlers_package

Handler=Callable[[dict[str,Any]],dict[str,Any]]
@dataclass(frozen=True,slots=True)
class RegisteredHandler:
    topic: str
    module: str
    handler: Handler

class ShopifyWebhookHandlerRegistry:
    def __init__(self) -> None:self._handlers: dict[str,RegisteredHandler]={}
    def register(self,topic: str,handler: Handler,module: str="manual") -> None:
        if not topic or not callable(handler):raise ValueError("topic et handler requis")
        if topic in self._handlers:raise ValueError(f"handler déjà enregistré: {topic}")
        self._handlers[topic]=RegisteredHandler(topic,module,handler)
    def load_defaults(self) -> int:
        loaded=0
        for info in pkgutil.iter_modules(handlers_package.__path__):
            if info.name.startswith('_') or info.name in {'base'}:continue
            module=importlib.import_module(f"{handlers_package.__name__}.{info.name}")
            topic=getattr(module,'TOPIC',None);handler=getattr(module,'handle',None)
            if topic and callable(handler) and topic not in self._handlers:
                self.register(str(topic),handler,module.__name__);loaded+=1
        return loaded
    def handle(self,topic: str,payload: dict[str,Any]) -> dict[str,Any]:
        registered=self._handlers.get(topic)
        if registered is None:return {"topic":topic,"action":"unhandled","payload":dict(payload),"warnings":("handler_missing",),"follow_up_operations":()}
        return registered.handler(payload)
    def topics(self) -> tuple[str,...]:return tuple(sorted(self._handlers))
    def snapshot(self) -> dict[str,object]:return {"count":len(self._handlers),"topics":self.topics()}
