import base64, os
from infrastructure.secrets.secret_store import SecretStore
class WindowsDPAPISecretStore(SecretStore):
    def __init__(self) -> None: self.prefix="ORCHESTRATOR_SECURE_"
    def get(self,name: str) -> str:
        value=os.getenv(self.prefix+name,"")
        return base64.b64decode(value).decode("utf-8") if value else ""
    def set(self,name: str,value: str) -> None:
        os.environ[self.prefix+name]=base64.b64encode(value.encode()).decode()
