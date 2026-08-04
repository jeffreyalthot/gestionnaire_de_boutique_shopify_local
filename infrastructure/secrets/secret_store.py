from abc import ABC, abstractmethod

class SecretStore(ABC):
    @abstractmethod
    def get(self, name: str) -> str:
        raise RuntimeError("La méthode doit être fournie par un gestionnaire de secrets concret.")

    @abstractmethod
    def set(self, name: str, value: str) -> None:
        raise RuntimeError("La méthode doit être fournie par un gestionnaire de secrets concret.")
