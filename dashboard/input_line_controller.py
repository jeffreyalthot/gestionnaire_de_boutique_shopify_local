from __future__ import annotations


class InputLineController:
    def __init__(self, prompt: str = '> ', max_length: int = 160) -> None:
        self.prompt = prompt
        self.max_length = max_length
        self.buffer = ''
        self.cursor = 0

    def insert(self, text: str) -> None:
        clean = text.replace('\r', '').replace('\n', '')
        available = self.max_length - len(self.buffer)
        clean = clean[:max(0, available)]
        self.buffer = self.buffer[:self.cursor] + clean + self.buffer[self.cursor:]
        self.cursor += len(clean)

    def backspace(self) -> None:
        if self.cursor:
            self.buffer = self.buffer[:self.cursor - 1] + self.buffer[self.cursor:]
            self.cursor -= 1

    def submit(self) -> str:
        value = self.buffer.strip()
        self.buffer = ''
        self.cursor = 0
        return value

    def render(self, width: int) -> str:
        return (self.prompt + self.buffer)[:width].ljust(width)
