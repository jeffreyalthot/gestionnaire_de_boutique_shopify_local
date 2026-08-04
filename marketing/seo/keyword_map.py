from __future__ import annotations
class KeywordMap:
    def assign(self, pages: list[str], keywords: list[str], *, max_per_page: int = 5) -> dict[str, tuple[str, ...]]:
        clean_pages = list(dict.fromkeys(page.strip() for page in pages if page.strip()))
        clean_keywords = list(dict.fromkeys(keyword.strip().lower() for keyword in keywords if keyword.strip()))
        if not clean_pages:
            return {}
        result: dict[str, list[str]] = {page: [] for page in clean_pages}
        for index, keyword in enumerate(clean_keywords):
            page = clean_pages[index % len(clean_pages)]
            if len(result[page]) < max(1, max_per_page):
                result[page].append(keyword)
        return {page: tuple(values) for page, values in result.items()}
