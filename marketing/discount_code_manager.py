from __future__ import annotations
import hashlib,re,secrets
from dataclasses import asdict,dataclass
from datetime import datetime,timezone

@dataclass(frozen=True,slots=True)
class DiscountCode:
    code: str
    prefix: str
    entropy_bits: int
    created_at: str
    campaign_id: str
    def as_dict(self):return asdict(self)

class DiscountCodeManager:
    ALPHABET="ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    def generate(self,prefix: str="ELIT",length: int=8) -> str:return self.create(prefix=prefix,length=length).code
    def create(self,*,prefix: str="ELIT",length: int=8,campaign_id: str="",existing: set[str]|None=None) -> DiscountCode:
        clean=re.sub(r"[^A-Z0-9]","",prefix.upper())[:8] or "SHOP";length=max(4,min(24,int(length)));existing=existing or set()
        for _ in range(20):
            suffix="".join(secrets.choice(self.ALPHABET) for _ in range(length));code=f"{clean}-{suffix}"
            if code not in existing:return DiscountCode(code,clean,length*5,datetime.now(timezone.utc).isoformat(),campaign_id)
        deterministic=hashlib.sha256(f"{clean}|{campaign_id}|{len(existing)}".encode()).hexdigest()[:length].upper();return DiscountCode(f"{clean}-{deterministic}",clean,length*4,datetime.now(timezone.utc).isoformat(),campaign_id)
    @staticmethod
    def valid(code: str) -> bool:return bool(re.fullmatch(r"[A-Z0-9]{1,8}-[A-Z0-9]{4,24}",str(code)))
