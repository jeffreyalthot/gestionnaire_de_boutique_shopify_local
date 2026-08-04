from __future__ import annotations
from abc import ABC,abstractmethod
from dataclasses import dataclass
@dataclass(frozen=True)
class TaxQuote:
    subtotal: float; tax: float; total: float; currency: str; source: str
class TaxProvider(ABC):
    @abstractmethod
    async def quote(self,subtotal: float,country: str,province: str='',currency: str='CAD')->TaxQuote:...
