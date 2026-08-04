from urllib.parse import urlencode
import secrets
from config.settings import Settings
from integrations.alibaba.gateway import AlibabaGateway

class AlibabaOAuth:
    def __init__(self,settings: Settings) -> None: self.settings=settings
    def authorization_url(self) -> tuple[str,str]:
        state=secrets.token_urlsafe(32)
        params={"response_type":"code","client_id":self.settings.alibaba_app_key,
                "redirect_uri":self.settings.alibaba_callback_url,"state":state,"view":"web","sp":"ICBU"}
        return self.settings.alibaba_oauth_url+"?"+urlencode(params),state
    async def exchange_code(self,code: str) -> dict[str,object]:
        gateway=AlibabaGateway(self.settings)
        try:
            return await gateway.call("taobao.top.auth.token.create",{"code":code},session_required=False)
        finally:
            await gateway.close()
    async def refresh(self,refresh_token: str) -> dict[str,object]:
        gateway=AlibabaGateway(self.settings)
        try:
            return await gateway.call("taobao.top.auth.token.refresh",{"refresh_token":refresh_token},session_required=False)
        finally:
            await gateway.close()
