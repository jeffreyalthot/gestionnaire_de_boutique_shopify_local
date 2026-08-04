from __future__ import annotations

import os
import select
import sys


class KeyboardHandler:
    commands = {"q": "quit", "r": "refresh", "1": "executive", "2": "catalog", "3": "orders", "4": "fulfillment", "5": "finance", "6": "marketing", "7": "compliance", "8": "system"}

    def action(self, key: str) -> str:
        return self.commands.get(key.lower(), "")

    def read_key(self) -> str:
        if not sys.stdin.isatty():
            return ""
        if os.name == "nt":
            import msvcrt
            if msvcrt.kbhit():
                key = msvcrt.getwch()
                if key in {"\x00", "\xe0"} and msvcrt.kbhit():
                    msvcrt.getwch()
                    return ""
                return key
            return ""
        readable, _, _ = select.select([sys.stdin], [], [], 0)
        return sys.stdin.read(1) if readable else ""
