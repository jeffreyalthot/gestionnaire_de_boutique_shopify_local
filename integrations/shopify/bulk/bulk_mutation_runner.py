from __future__ import annotations
class BulkMutationRunner:
    def __init__(self,transport)->None:self.transport=transport
    async def run(self,mutation: str,staged_upload_path: str)->dict:
        data=await self.transport.execute('mutation Run($mutation:String!,$path:String!){bulkOperationRunMutation(mutation:$mutation,stagedUploadPath:$path){bulkOperation{id status type} userErrors{field message code}}}',{'mutation':mutation,'path':staged_upload_path})
        node=data['bulkOperationRunMutation']
        if node.get('userErrors'):raise ValueError(str(node['userErrors']))
        return node['bulkOperation']
