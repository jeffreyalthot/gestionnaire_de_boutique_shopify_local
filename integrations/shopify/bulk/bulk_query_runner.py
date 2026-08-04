from __future__ import annotations
class BulkQueryRunner:
    def __init__(self,transport)->None:self.transport=transport
    async def run(self,query: str)->dict:
        data=await self.transport.execute('mutation Run($query:String!){bulkOperationRunQuery(query:$query){bulkOperation{id status type} userErrors{field message code}}}',{'query':query})
        node=data['bulkOperationRunQuery']
        if node.get('userErrors'):raise ValueError(str(node['userErrors']))
        return node['bulkOperation']
