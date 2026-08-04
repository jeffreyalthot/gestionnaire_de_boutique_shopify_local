from __future__ import annotations
from integrations.shopify.files_client import ShopifyFilesClient
class ShopifyMediaClient:
    def __init__(self,files: ShopifyFilesClient)->None:self.files=files
    async def stage_product_images(self,images: list[dict])->dict:
        inputs=[{'resource':'IMAGE','filename':item['filename'],'mimeType':item.get('mime_type','image/jpeg'),'httpMethod':'POST'} for item in images]
        return await self.files.staged_uploads(inputs)
