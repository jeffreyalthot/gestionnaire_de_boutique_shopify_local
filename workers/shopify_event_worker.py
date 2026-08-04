class ShopifyEventWorker:
    def __init__(self,service) -> None: self.service=service
    async def run(self,payload: dict[str,object]) -> object:
        method=getattr(self.service,"shopify_event",None) or getattr(self.service,"execute",None)
        if method is None: raise AttributeError("Le service ne fournit pas l'action requise.")
        result=method(payload)
        if hasattr(result,"__await__"): return await result
        return result
