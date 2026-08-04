from localization.translation_memory import TranslationMemory


class ProductTranslation:
    def __init__(self,memory: TranslationMemory) -> None: self.memory=memory
    def translate_fields(self, product: dict[str,object], source_locale: str, target_locale: str) -> dict[str,object]:
        result=dict(product)
        for key in ("title","description","seo_title","seo_description"):
            value=str(product.get(key,"")); translated=self.memory.get(value,source_locale,target_locale)
            if translated: result[key]=translated
        return result
