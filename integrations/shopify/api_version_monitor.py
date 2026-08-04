from __future__ import annotations
from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True)
class ApiVersionStatus:
    configured: str; latest_supported: str; supported: bool; upgrade_recommended: bool
class ApiVersionMonitor:
    def evaluate(self,configured: str,versions: list[dict])->ApiVersionStatus:
        supported=sorted(str(v.get('handle')) for v in versions if v.get('supported'))
        latest=supported[-1] if supported else ''
        return ApiVersionStatus(configured,latest,configured in supported,bool(latest and configured!=latest))
