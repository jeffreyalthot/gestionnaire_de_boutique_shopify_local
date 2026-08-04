from __future__ import annotations

import re
from dataclasses import dataclass, field
from string import Template
from threading import RLock
from typing import Mapping


class TemplateRenderError(ValueError):
    """Raised when a registered template cannot be rendered safely."""


@dataclass(frozen=True, slots=True)
class TemplateDefinition:
    name: str
    template: str
    required: tuple[str, ...] = ()
    defaults: Mapping[str, object] = field(default_factory=dict)
    maximum_length: int = 10_000


class TemplateEngine:
    """Small deterministic template engine suitable for a 2 GB runtime.

    It intentionally uses :class:`string.Template` instead of a large templating
    dependency. Registered templates can declare required variables and defaults.
    The historical ``render(template, values)`` method remains supported.
    """

    _whitespace = re.compile(r"[ \t]+")

    def __init__(self) -> None:
        self._templates: dict[str, TemplateDefinition] = {}
        self._lock = RLock()

    def register(
        self,
        name: str,
        template: str,
        *,
        required: tuple[str, ...] = (),
        defaults: Mapping[str, object] | None = None,
        maximum_length: int = 10_000,
        replace: bool = False,
    ) -> None:
        name = str(name).strip()
        if not name:
            raise ValueError("template name is required")
        if not isinstance(template, str) or not template:
            raise ValueError("template text is required")
        definition = TemplateDefinition(
            name=name,
            template=template,
            required=tuple(dict.fromkeys(str(item) for item in required)),
            defaults=dict(defaults or {}),
            maximum_length=max(64, int(maximum_length)),
        )
        with self._lock:
            if name in self._templates and not replace:
                raise ValueError(f"template already registered: {name}")
            self._templates[name] = definition

    def unregister(self, name: str) -> bool:
        with self._lock:
            return self._templates.pop(name, None) is not None

    def names(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(sorted(self._templates))

    def render(self, template: str, values: Mapping[str, object]) -> str:
        """Render an ad-hoc template while preserving missing placeholders."""
        converted = {str(key): self._stringify(value) for key, value in values.items()}
        return Template(str(template)).safe_substitute(converted)

    def render_named(self, name: str, values: Mapping[str, object] | None = None) -> str:
        with self._lock:
            definition = self._templates.get(name)
        if definition is None:
            raise KeyError(name)
        merged = dict(definition.defaults)
        merged.update(dict(values or {}))
        missing = [key for key in definition.required if key not in merged or merged[key] in (None, "")]
        if missing:
            raise TemplateRenderError(f"missing template values: {', '.join(missing)}")
        rendered = self.render(definition.template, merged)
        rendered = self.normalize_whitespace(rendered)
        if len(rendered) > definition.maximum_length:
            raise TemplateRenderError(
                f"rendered template exceeds {definition.maximum_length} characters"
            )
        return rendered

    @classmethod
    def normalize_whitespace(cls, text: str) -> str:
        lines = [cls._whitespace.sub(" ", line).strip() for line in str(text).splitlines()]
        return "\n".join(line for line in lines if line).strip()

    @staticmethod
    def _stringify(value: object) -> str:
        if value is None:
            return ""
        if isinstance(value, bool):
            return "oui" if value else "non"
        return str(value)
