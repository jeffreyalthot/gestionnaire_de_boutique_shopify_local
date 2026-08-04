from infrastructure.secrets.secret_store import SecretStore
class KeyringSecretStore(SecretStore):
    def __init__(self,service: str="shopify-alibaba-orchestrator") -> None: self.service=service
    def get(self,name: str) -> str:
        try:
            import keyring
            return keyring.get_password(self.service,name) or ""
        except ImportError:
            return ""
    def set(self,name: str,value: str) -> None:
        try:
            import keyring
        except ImportError as exc:
            raise RuntimeError("Le paquet keyring est requis pour ce fournisseur.") from exc
        keyring.set_password(self.service,name,value)
