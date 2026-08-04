from __future__ import annotations

import re


class ResponseTemplateEngine:
    TOKEN = re.compile(r"\{([a-zA-Z0-9_]+)\}")

    def render(self, template: str, values: dict[str, object]) -> str:
        def replace(match: re.Match[str]) -> str:
            key = match.group(1)
            return str(values.get(key, ""))
        text = self.TOKEN.sub(replace, template)
        return re.sub(r"\s+", " ", text).strip()
