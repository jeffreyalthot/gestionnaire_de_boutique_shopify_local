from __future__ import annotations

import re


class QueryBuilder:
    STOP_WORDS = {"the", "a", "an", "and", "or", "for", "with", "de", "la", "le", "les", "et", "pour"}

    def build(self, seed: str, *, include: list[str] | None = None, exclude: list[str] | None = None) -> list[str]:
        tokens = [token for token in re.findall(r"[\w-]+", seed.lower()) if token not in self.STOP_WORDS]
        tokens.extend(item.strip().lower() for item in (include or []) if item.strip())
        base = " ".join(dict.fromkeys(tokens))
        queries = [base]
        for suffix in ("dropshipping", "ready to ship", "low moq"):
            queries.append(f"{base} {suffix}".strip())
        exclusions = {item.lower().strip() for item in (exclude or [])}
        return [query for query in queries if query and not any(term in query for term in exclusions)]
