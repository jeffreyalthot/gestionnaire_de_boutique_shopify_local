import json
from security.encryption import EncryptionService

class FieldEncryption:
    def __init__(self, service: EncryptionService) -> None:
        self.service = service
    def encrypt_mapping(self, data: dict[str, object]) -> str:
        return self.service.encrypt(json.dumps(data, ensure_ascii=False, separators=(",", ":"), default=str))
    def decrypt_mapping(self, value: str) -> dict[str, object]:
        return json.loads(self.service.decrypt(value))
