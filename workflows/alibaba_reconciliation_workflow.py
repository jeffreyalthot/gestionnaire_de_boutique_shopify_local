from integrations.alibaba.client import AlibabaClient
class AlibabaReconciliationWorkflow:
    def __init__(self,client: AlibabaClient) -> None: self.client=client
    async def execute(self) -> dict[str,object]: return await self.client.orders(page=1,page_size=50)
