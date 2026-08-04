import hashlib, re


class ErrorFingerprint:
    def build(self, exc: BaseException, operation: str="") -> str:
        message=re.sub(r"\b[0-9a-fA-F]{8,}\b","<id>",str(exc)); material=f"{operation}|{type(exc).__name__}|{message}"
        return hashlib.sha256(material.encode()).hexdigest()[:24]
