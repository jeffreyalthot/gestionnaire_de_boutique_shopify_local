from __future__ import annotations
import asyncio,time
class BulkOperationMonitor:
    TERMINAL={'COMPLETED','FAILED','CANCELED','EXPIRED'}
    def __init__(self,transport,poll_seconds: float=5,timeout_seconds: float=3600)->None:self.transport=transport;self.poll=poll_seconds;self.timeout=timeout_seconds
    async def wait(self,operation_id: str)->dict:
        started=time.monotonic()
        while time.monotonic()-started<self.timeout:
            data=await self.transport.execute('query Bulk($id:ID!){node(id:$id){... on BulkOperation{id status errorCode objectCount fileSize url partialDataUrl}}}',{'id':operation_id})
            node=data.get('node') or {}
            if node.get('status') in self.TERMINAL:return node
            await asyncio.sleep(self.poll)
        raise TimeoutError('Opération bulk Shopify expirée localement.')
