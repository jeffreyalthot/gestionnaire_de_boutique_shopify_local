from __future__ import annotations
from integrations.shopify.graphql_document_loader import GraphQLDocumentLoader
class ShopifyFilesClient:
    def __init__(self,transport,loader: GraphQLDocumentLoader|None=None)->None:self.transport=transport;self.loader=loader or GraphQLDocumentLoader()
    async def staged_uploads(self,inputs: list[dict])->dict:return await self.transport.execute(self.loader.load('files/staged_uploads_create.graphql'),{'input':inputs})
    async def create(self,files: list[dict])->dict:return await self.transport.execute(self.loader.load('files/file_create.graphql'),{'files':files})
