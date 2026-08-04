from __future__ import annotations

from catalog.normalization.color_normalizer import ColorNormalizer


class OptionNormalizer:
    NAMES = {"colour": "Color", "color": "Color", "couleur": "Color", "size": "Size", "taille": "Size",
             "material": "Material", "matériau": "Material", "style": "Style"}

    def __init__(self) -> None:
        self.colors = ColorNormalizer()

    def normalize(self, options: dict[str, object]) -> dict[str, str]:
        result: dict[str, str] = {}
        for key, value in options.items():
            name = self.NAMES.get(str(key).casefold().strip(), str(key).strip().title()[:50])
            text = " ".join(str(value).split())[:100]
            result[name] = self.colors.normalize(text) if name == "Color" else text
        return result
