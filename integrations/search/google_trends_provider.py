from __future__ import annotations
from integrations.search.search_provider import SearchProvider,SearchSignal
class GoogleTrendsProvider(SearchProvider):
    """Adaptateur injecté; aucune collecte non autorisée n'est effectuée directement."""
    def __init__(self,fetcher=None)->None:self.fetcher=fetcher
    async def signals(self,terms: list[str])->list[SearchSignal]:
        if self.fetcher is None:return [SearchSignal(term,0.0,'google_trends_unconfigured',{}) for term in terms]
        values=self.fetcher(terms)
        if hasattr(values,'__await__'):values=await values
        return [SearchSignal(term,max(0,min(1,float(values.get(term,0))/100)),'google_trends',{'interest':values.get(term,0)}) for term in terms]
