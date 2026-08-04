from __future__ import annotations

import io
import sys
from contextlib import AbstractContextManager
from threading import RLock
from typing import Callable


class _CapturedStream(io.TextIOBase):
    def __init__(self, sink: Callable[[str], None]) -> None:
        self.sink = sink
        self._buffer = ""

    def write(self, text: str) -> int:
        self._buffer += str(text)
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            if line.strip():
                self.sink(line.replace("\r", " ")[:1000])
        return len(text)

    def flush(self) -> None:
        if self._buffer.strip():
            self.sink(self._buffer.replace("\r", " ")[:1000])
            self._buffer = ""


class StdoutGuard(AbstractContextManager["StdoutGuard"]):
    """Redirige les sorties parasites vers l'anneau fixe du terminal."""

    _lock = RLock()

    def __init__(self, sink: Callable[[str], None]) -> None:
        self.sink = sink
        self._stdout: io.TextIOBase | None = None
        self._stderr: io.TextIOBase | None = None

    def __enter__(self) -> "StdoutGuard":
        self._lock.acquire()
        self._stdout, self._stderr = sys.stdout, sys.stderr
        sys.stdout = _CapturedStream(self.sink)
        sys.stderr = _CapturedStream(lambda line: self.sink(f"ERROR {line}"))
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        sys.stdout.flush()
        sys.stderr.flush()
        assert self._stdout is not None and self._stderr is not None
        sys.stdout, sys.stderr = self._stdout, self._stderr
        self._lock.release()
