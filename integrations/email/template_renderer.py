from __future__ import annotations
import re
TOKEN=re.compile(r'\{\{\s*([a-zA-Z0-9_.-]+)\s*\}\}')
class TemplateRenderer:
    def render(self,template: str,context: dict)->str:
        def replace(match):
            value=context
            for part in match.group(1).split('.'):
                value=value.get(part,'') if isinstance(value,dict) else ''
            return str(value)
        return TOKEN.sub(replace,template)
