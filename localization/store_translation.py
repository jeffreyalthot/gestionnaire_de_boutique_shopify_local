from __future__ import annotations

from dataclasses import asdict, dataclass

from localization.translation_memory import TranslationMemory


@dataclass(frozen=True, slots=True)
class StoreTranslationResult:
    text: str
    translated: bool
    source_locale: str
    target_locale: str
    missing: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class StoreTranslation:
    def __init__(self, memory: TranslationMemory) -> None:
        self.memory = memory

    def resolve(self, text: str, source: str, target: str) -> str:
        return self.resolve_details(text, source, target).text

    def resolve_details(self, text: str, source: str, target: str, *, fallback: str | None = None) -> StoreTranslationResult:
        if source == target:
            return StoreTranslationResult(text, False, source, target, False)
        translated = self.memory.get(text, source, target)
        value = translated if translated is not None else (fallback if fallback is not None else text)
        return StoreTranslationResult(value, translated is not None, source, target, translated is None)

    def translate_mapping(self, values: dict[str, str], source: str, target: str) -> tuple[dict[str, str], tuple[str, ...]]:
        output: dict[str, str] = {}; missing: list[str] = []
        for key, text in values.items():
            result = self.resolve_details(text, source, target)
            output[key] = result.text
            if result.missing:
                missing.append(key)
        return output, tuple(missing)
