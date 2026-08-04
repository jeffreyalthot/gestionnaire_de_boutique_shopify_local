from __future__ import annotations

import pickle
from pathlib import Path


def load_model(path: Path):
    if not path.is_file():
        raise FileNotFoundError(path)
    try:
        import joblib
    except ImportError:
        with path.open("rb") as handle:
            return pickle.load(handle)
    return joblib.load(path)
