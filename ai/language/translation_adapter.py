from __future__ import annotations

from collections import OrderedDict
from dataclasses import asdict, dataclass
from threading import RLock
from typing import Callable

from ai.language.text_sanitizer import sanitize

TranslationProvider = Callable[[str, str, str], str]


@dataclass(frozen=True, slots=True)
class TranslationResult:
    text: str
    source: str
    target: str
    provider: str
    cached: bool = False

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class TranslationAdapter:
    """Provider-based translation with a tiny bounded in-memory cache."""

    _builtin = {
        ("fr", "en"): {
            "bonjour": "hello",
            "commande": "order",
            "expédiée": "shipped",
            "remboursement": "refund",
            "merci": "thank you",
        },
        ("en", "fr"): {
            "hello": "bonjour",
            "order": "commande",
            "shipped": "expédiée",
            "refund": "remboursement",
            "thank you": "merci",
        },
    }

    def __init__(self, *, maximum_cache_entries: int = 256) -> None:
        self.maximum_cache_entries = max(0, int(maximum_cache_entries))
        self._providers: dict[tuple[str, str], tuple[str, TranslationProvider]] = {}
        self._cache: OrderedDict[tuple[str, str, str], TranslationResult] = OrderedDict()
        self._lock = RLock()

    @staticmethod
    def normalize_locale(value: str) -> str:
        return str(value).strip().lower().replace("_", "-").split("-", 1)[0]

    def register(self, source: str, target: str, provider: TranslationProvider, *, name: str = "custom") -> None:
        if not callable(provider):
            raise TypeError("provider must be callable")
        pair = (self.normalize_locale(source), self.normalize_locale(target))
        if pair[0] == pair[1]:
            raise ValueError("source and target must differ")
        with self._lock:
            self._providers[pair] = (str(name), provider)
            self._cache.clear()

    def translate(self, text: str, source: str, target: str) -> str:
        return self.translate_with_metadata(text, source, target).text

    def translate_with_metadata(self, text: str, source: str, target: str) -> TranslationResult:
        source_code = self.normalize_locale(source)
        target_code = self.normalize_locale(target)
        clean = sanitize(text, 20_000)
        if source_code == target_code:
            return TranslationResult(clean, source_code, target_code, "identity")
        key = (clean, source_code, target_code)
        with self._lock:
            cached = self._cache.get(key)
            if cached is not None:
                self._cache.move_to_end(key)
                return TranslationResult(cached.text, source_code, target_code, cached.provider, True)
            provider_entry = self._providers.get((source_code, target_code))
        if provider_entry is not None:
            name, provider = provider_entry
            translated = sanitize(provider(clean, source_code, target_code), 20_000)
            result = TranslationResult(translated, source_code, target_code, name)
        elif (source_code, target_code) in self._builtin:
            translated = self._dictionary_translate(clean, self._builtin[(source_code, target_code)])
            result = TranslationResult(translated, source_code, target_code, "builtin_dictionary")
        else:
            raise RuntimeError("Aucun modèle de traduction local n'est chargé pour cette paire linguistique.")
        self._remember(key, result)
        return result

    def _remember(self, key: tuple[str, str, str], result: TranslationResult) -> None:
        if self.maximum_cache_entries <= 0:
            return
        with self._lock:
            self._cache[key] = result
            self._cache.move_to_end(key)
            while len(self._cache) > self.maximum_cache_entries:
                self._cache.popitem(last=False)

    @staticmethod
    def _dictionary_translate(text: str, dictionary: dict[str, str]) -> str:
        result = text
        for source, target in sorted(dictionary.items(), key=lambda item: len(item[0]), reverse=True):
            result = result.replace(source, target).replace(source.capitalize(), target.capitalize())
        return result
