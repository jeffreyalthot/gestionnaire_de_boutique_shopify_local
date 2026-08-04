import json
from pathlib import Path
from infrastructure.secrets.secret_store import SecretStore
from security.encryption import EncryptionService
class EncryptedFileSecretStore(SecretStore):
    def __init__(self,path: Path,encryption: EncryptionService) -> None: self.path=path; self.encryption=encryption
    def _load(self) -> dict[str,str]:
        if not self.path.exists(): return {}
        return json.loads(self.encryption.decrypt(self.path.read_text(encoding="utf-8")))
    def get(self,name: str) -> str: return self._load().get(name,"")
    def set(self,name: str,value: str) -> None:
        data=self._load(); data[name]=value; self.path.parent.mkdir(parents=True,exist_ok=True)
        self.path.write_text(self.encryption.encrypt(json.dumps(data)),encoding="utf-8")
