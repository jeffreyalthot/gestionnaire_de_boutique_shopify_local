from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ChannelPublicationPlan:
    channel: str
    product_ids: tuple[str,...]
    dry_run: bool=True
