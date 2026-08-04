from __future__ import annotations

from dataclasses import asdict
from marketing.campaign import Campaign


class CampaignRepository:
    def __init__(self) -> None: self._items: dict[str,Campaign]={}
    def save(self,campaign: Campaign) -> None: self._items[campaign.id]=campaign
    def get(self,campaign_id: str) -> Campaign | None: return self._items.get(campaign_id)
    def list(self,status: str | None=None) -> tuple[Campaign,...]: return tuple(x for x in self._items.values() if status is None or x.status==status)
    def snapshot(self) -> list[dict[str,object]]: return [asdict(x) for x in self._items.values()]
