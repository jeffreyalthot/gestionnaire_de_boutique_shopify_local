from __future__ import annotations
import hashlib
import hmac
from urllib.parse import urlencode

class AlibabaSigner:
    def __init__(self,app_secret: str,sign_method: str="hmac") -> None:
        if not app_secret: raise ValueError("APP_SECRET Alibaba obligatoire.")
        self.secret=app_secret; self.sign_method=sign_method.lower()

    @staticmethod
    def canonical(params: dict[str,object]) -> str:
        return "".join(f"{key}{params[key]}" for key in sorted(params) if key!="sign" and params[key] is not None)

    def sign(self,params: dict[str,object]) -> str:
        canonical=self.canonical(params).encode("utf-8")
        secret=self.secret.encode("utf-8")
        if self.sign_method=="md5":
            return hashlib.md5(secret+canonical+secret).hexdigest().upper()
        return hmac.new(secret,canonical,hashlib.md5).hexdigest().upper()

    def signed_params(self,params: dict[str,object]) -> dict[str,object]:
        result={k:v for k,v in params.items() if v is not None}
        result["sign"]=self.sign(result)
        return result
