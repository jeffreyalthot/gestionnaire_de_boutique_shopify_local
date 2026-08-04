from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class FeatureFlags:
    live_shopify_writes: bool
    live_alibaba_orders: bool
    live_alibaba_payments: bool
    ai_online_learning: bool
    rest_compatibility: bool
