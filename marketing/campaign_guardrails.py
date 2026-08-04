from dataclasses import dataclass
from marketing.campaign import Campaign


@dataclass(frozen=True, slots=True)
class CampaignDecision:
    allowed: bool
    issues: tuple[str,...]


class CampaignGuardrails:
    def validate(self,campaign: Campaign,*,available_budget_cad: float,min_duration_minutes: int=30) -> CampaignDecision:
        issues=[]
        if campaign.budget_cad<=0: issues.append("invalid_budget")
        if campaign.budget_cad>available_budget_cad: issues.append("budget_exceeded")
        if campaign.ends_at<=campaign.starts_at: issues.append("invalid_window")
        elif (campaign.ends_at-campaign.starts_at).total_seconds()<min_duration_minutes*60: issues.append("window_too_short")
        if not campaign.channel: issues.append("missing_channel")
        return CampaignDecision(not issues,tuple(issues))
