from __future__ import annotations

import re


class SearchTermBuilder:
    STOP = {"the", "and", "for", "with", "pour", "avec", "des", "les", "une", "un"}

    def build(self, title: str, attributes: dict[str, object], maximum: int = 20) -> tuple[str, ...]:
        tokens = re.findall(r"[\w-]{3,}", " ".join([title, *map(str, attributes.values())]).casefold())
        unique = []
        for token in tokens:
            if token not in self.STOP and token not in unique:
                unique.append(token)
        return tuple(unique[:maximum])
