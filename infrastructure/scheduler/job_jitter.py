from __future__ import annotations
import hashlib
class JobJitter:
    @staticmethod
    def seconds(job_name: str,maximum: int)->int:
        if maximum<=0:return 0
        return int.from_bytes(hashlib.sha256(job_name.encode()).digest()[:4],'big')%(maximum+1)
