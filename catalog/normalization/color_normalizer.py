from __future__ import annotations


class ColorNormalizer:
    MAP = {"grey": "Gray", "gray": "Gray", "black": "Black", "white": "White", "red": "Red",
           "blue": "Blue", "green": "Green", "yellow": "Yellow", "pink": "Pink", "purple": "Purple",
           "brown": "Brown", "orange": "Orange", "transparent": "Clear", "clear": "Clear"}

    def normalize(self, value: str) -> str:
        key = " ".join(value.casefold().split())
        return self.MAP.get(key, value.strip().title()[:50] or "Unspecified")
