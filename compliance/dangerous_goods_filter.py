from __future__ import annotations

import re
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class DangerousGoodsAssessment:
    category: str
    indicators: tuple[str,...]
    restricted: bool
    carrier_review_required: bool
    shipping_mode: str
    def as_dict(self):return asdict(self)

class DangerousGoodsFilter:
    PATTERNS={"battery":r"lithium|li-ion|battery|batterie","chemical":r"flammable|corrosive|toxic|solvent|inflammable","compressed gas":r"aerosol|compressed gas|gaz comprimé","magnet":r"strong magnet|aimant puissant","dry ice":r"dry ice|glace carbonique"}
    def assess(self,text: str) -> DangerousGoodsAssessment:
        indicators=tuple(name for name,pattern in self.PATTERNS.items() if re.search(pattern,str(text),re.I)); category=indicators[0] if indicators else ""; restricted=category in {"chemical","compressed gas","dry ice"}; review=bool(indicators); mode="ground_only" if category in {"battery","magnet"} else "specialized_carrier" if restricted else "standard"
        return DangerousGoodsAssessment(category,indicators,restricted,review,mode)

def dangerous_goods_reason(text: str) -> str:return DangerousGoodsFilter().assess(text).category
