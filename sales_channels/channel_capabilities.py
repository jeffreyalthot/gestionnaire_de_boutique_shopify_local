from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ChannelCapabilities:
    products: bool=True
    inventory: bool=True
    orders: bool=False
    returns: bool=False
    translations: bool=False
