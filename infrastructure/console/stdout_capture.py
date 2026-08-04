from __future__ import annotations
from io import TextIOBase
from typing import Any


class StdoutCapture(TextIOBase):
    def __init__(self, sink: Any, level: str = 'INFO') -> None:
        self.sink=sink; self.level=level; self._buffer=''
    def write(self, value: str) -> int:
        self._buffer += value
        while '\n' in self._buffer:
            line,self._buffer=self._buffer.split('\n',1)
            if line: self.sink.publish(line,self.level)
        return len(value)
    def flush(self) -> None:
        if self._buffer: self.sink.publish(self._buffer,self.level); self._buffer=''
    def isatty(self) -> bool: return False
