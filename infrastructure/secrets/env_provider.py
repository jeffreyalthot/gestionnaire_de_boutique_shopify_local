import os
from infrastructure.secrets.secret_store import SecretStore
class EnvSecretStore(SecretStore):
    def get(self,name: str) -> str: return os.getenv(name,"")
    def set(self,name: str,value: str) -> None: os.environ[name]=value
