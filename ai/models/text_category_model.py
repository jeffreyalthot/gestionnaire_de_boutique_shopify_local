from __future__ import annotations
from ai.models.online_classifier import OnlineTextClassifier

class TextCategoryModel(OnlineTextClassifier):
    CATEGORIES=("general","electronics","home","fashion","beauty","sports","automotive")
    KEYWORDS={"electronics":("usb","bluetooth","battery","charger","electronic"),"home":("kitchen","home","decor","lamp"),"fashion":("shirt","dress","shoe","apparel"),"beauty":("beauty","skin","cosmetic","hair"),"sports":("sport","fitness","gym","outdoor"),"automotive":("car","auto","vehicle","motor")}
    def __init__(self) -> None:super().__init__(list(self.CATEGORIES))
    def classify(self,text: str) -> tuple[str,float]:
        if self.fitted:return self.predict(text)
        lowered=text.lower(); hits={cat:sum(word in lowered for word in words) for cat,words in self.KEYWORDS.items()}; best=max(hits,key=hits.get)
        return (best,min(1.0,.55+.1*hits[best])) if hits[best] else ("general",.4)
