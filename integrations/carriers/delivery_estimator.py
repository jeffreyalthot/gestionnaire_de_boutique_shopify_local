from __future__ import annotations
from datetime import date,timedelta
class DeliveryEstimator:
    def estimate(self,ship_date: date,min_days: int,max_days: int,buffer_days: int=2)->dict[str,str|int]:
        minimum=max(0,min_days);maximum=max(minimum,max_days)+max(0,buffer_days)
        return {'earliest':(ship_date+timedelta(days=minimum)).isoformat(),'latest':(ship_date+timedelta(days=maximum)).isoformat(),'window_days':maximum-minimum}
