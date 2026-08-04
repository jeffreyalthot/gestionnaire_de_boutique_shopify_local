from contextlib import contextmanager
from time import perf_counter
from typing import Iterator

@contextmanager
def timer(callback) -> Iterator[None]:
    started = perf_counter()
    try:
        yield
    finally:
        callback(perf_counter() - started)
