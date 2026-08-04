from __future__ import annotations
import httpx
class StagedUploads:
    def __init__(self,client: httpx.AsyncClient|None=None)->None:self.client=client
    async def upload(self,target: dict,data: bytes,filename: str,content_type: str)->str:
        owns=self.client is None;client=self.client or httpx.AsyncClient(timeout=60)
        try:
            fields={item['name']:item['value'] for item in target.get('parameters',[])}
            response=await client.post(target['url'],data=fields,files={'file':(filename,data,content_type)});response.raise_for_status();return str(target.get('resourceUrl',''))
        finally:
            if owns:await client.aclose()
