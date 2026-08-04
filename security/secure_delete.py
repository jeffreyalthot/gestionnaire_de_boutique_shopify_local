from pathlib import Path
def secure_delete(path: Path) -> None:
    if not path.exists() or not path.is_file():
        return
    size = path.stat().st_size
    with path.open("r+b") as handle:
        handle.write(b"\x00" * size)
        handle.flush()
    path.unlink()
