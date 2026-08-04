from __future__ import annotations
import ipaddress,socket
from urllib.parse import urlparse
import httpx
class UnsafeDownloadUrl(ValueError): pass
class DownloadClient:
    def __init__(self,max_bytes: int=12582912,allowed_hosts: set[str]|None=None)->None: self.max_bytes=max_bytes; self.allowed_hosts=allowed_hosts or set()
    def validate_url(self,url: str)->str:
        parsed=urlparse(url)
        if parsed.scheme!='https' or not parsed.hostname: raise UnsafeDownloadUrl('HTTPS et hôte requis.')
        host=parsed.hostname.lower()
        if self.allowed_hosts and host not in self.allowed_hosts: raise UnsafeDownloadUrl('Hôte non autorisé.')
        for item in socket.getaddrinfo(host,443,type=socket.SOCK_STREAM):
            ip=ipaddress.ip_address(item[4][0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved: raise UnsafeDownloadUrl('Adresse réseau privée interdite.')
        return host
    async def download(self,url: str)->tuple[bytes,str]:
        self.validate_url(url); data=bytearray(); content_type=''
        async with httpx.AsyncClient(follow_redirects=False,timeout=30) as client:
            async with client.stream('GET',url) as response:
                response.raise_for_status(); content_type=response.headers.get('content-type','').split(';',1)[0]
                async for chunk in response.aiter_bytes():
                    data.extend(chunk)
                    if len(data)>self.max_bytes: raise ValueError('Téléchargement trop volumineux.')
        return bytes(data),content_type
