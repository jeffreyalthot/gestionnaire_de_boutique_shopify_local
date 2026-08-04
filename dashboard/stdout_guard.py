from __future__ import annotations

import io
from contextlib import redirect_stderr, redirect_stdout
from typing import Iterator


class CapturedOutput:
    def __init__(self) -> None:
        self.buffer = io.StringIO()

    def __enter__(self) -> "CapturedOutput":
        self._stdout = redirect_stdout(self.buffer)
        self._stderr = redirect_stderr(self.buffer)
        self._stdout.__enter__(); self._stderr.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self._stderr.__exit__(exc_type, exc, tb); self._stdout.__exit__(exc_type, exc, tb)

    def text(self) -> str:
        return self.buffer.getvalue()
