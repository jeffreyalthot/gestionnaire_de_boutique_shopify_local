from __future__ import annotations
import hashlib
from dataclasses import asdict,dataclass
from pathlib import PurePosixPath

@dataclass(frozen=True,slots=True)
class ThemeAssetDecision:
    allowed: bool
    reason: str
    normalized_path: str
    size_bytes: int
    extension: str
    sha256: str
    def as_dict(self):return asdict(self)

class ThemeAssetGuard:
    ALLOWED={".liquid",".json",".css",".js",".png",".jpg",".jpeg",".svg",".woff2"}
    def validate(self,path: str,size_bytes: int) -> tuple[bool,str]:
        result=self.inspect(path,size_bytes);return result.allowed,result.reason
    def inspect(self,path: str,size_bytes: int,*,content: bytes|None=None,maximum_bytes: int=20*1024*1024) -> ThemeAssetDecision:
        p=PurePosixPath(str(path).replace("\\","/"));size=max(0,int(size_bytes));reason="allowed";allowed=True
        if p.is_absolute() or ".." in p.parts:allowed=False;reason="unsafe_path"
        elif p.suffix.lower() not in self.ALLOWED:allowed=False;reason="unsupported_type"
        elif size>maximum_bytes:allowed=False;reason="too_large"
        elif content is not None and len(content)!=size:allowed=False;reason="size_mismatch"
        digest=hashlib.sha256(content).hexdigest() if content is not None else ""
        return ThemeAssetDecision(allowed,reason,str(p),size,p.suffix.lower(),digest)
