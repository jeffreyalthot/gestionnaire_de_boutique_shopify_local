from __future__ import annotations
from collections import Counter
from integrations.search.search_provider import SearchProvider,SearchSignal
class KeywordProvider(SearchProvider):
    def __init__(self,documents: list[str]|None=None)->None:self.documents=documents or []
    async def signals(self,terms: list[str])->list[SearchSignal]:
        corpus=' '.join(self.documents).lower();counts=Counter(corpus.split());maximum=max(counts.values(),default=1)
        return [SearchSignal(term,counts[term.lower()]/maximum,'local_keywords',{'count':counts[term.lower()]}) for term in terms]
