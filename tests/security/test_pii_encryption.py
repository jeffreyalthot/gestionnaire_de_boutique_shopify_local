from security.encryption import EncryptionService
def test_encryption_roundtrip():
    e=EncryptionService("key"); x=e.encrypt("secret"); assert x!="secret" and e.decrypt(x)=="secret"
