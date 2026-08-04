from security.field_encryption import FieldEncryption

class PIIVault:
    def __init__(self, encryption: FieldEncryption) -> None:
        self.encryption = encryption
    def store_address(self, address: dict[str, object]) -> str:
        return self.encryption.encrypt_mapping(address)
    def read_address(self, encrypted: str) -> dict[str, object]:
        return self.encryption.decrypt_mapping(encrypted)
