from analytics.attribution.channel_attribution import ChannelAttribution


class CampaignAttribution(ChannelAttribution):
    def allocate_campaigns(self, touchpoints, revenue: float, *, model: str = "linear"):
        normalized = [{**item, "channel": item.get("campaign", "unknown")} for item in touchpoints]
        return self.allocate(normalized, revenue, model=model)
