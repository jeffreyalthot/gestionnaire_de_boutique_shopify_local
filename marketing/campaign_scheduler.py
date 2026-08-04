from __future__ import annotations
from dataclasses import asdict,dataclass
from datetime import datetime,timezone
from marketing.campaign import Campaign

@dataclass(frozen=True,slots=True)
class CampaignScheduleDecision:
    campaign_id: str
    due: bool
    active: bool
    reason: str
    seconds_until_start: float
    seconds_until_end: float
    def as_dict(self):return asdict(self)

class CampaignScheduler:
    def due(self,campaigns: list[Campaign]|tuple[Campaign,...],now: datetime|None=None) -> tuple[Campaign,...]:return tuple(c for c in campaigns if self.evaluate(c,now=now).due)
    def evaluate(self,campaign: Campaign,*,now: datetime|None=None) -> CampaignScheduleDecision:
        current=now or datetime.now(timezone.utc);start=campaign.starts_at;end=campaign.ends_at
        if start.tzinfo is None:start=start.replace(tzinfo=timezone.utc)
        if end.tzinfo is None:end=end.replace(tzinfo=timezone.utc)
        active=start<=current<end;approved=campaign.status in {"approved","scheduled"};due=active and approved;reason="due" if due else "not_approved" if not approved else "not_started" if current<start else "ended"
        return CampaignScheduleDecision(str(campaign.id),due,active,reason,round((start-current).total_seconds(),2),round((end-current).total_seconds(),2))
