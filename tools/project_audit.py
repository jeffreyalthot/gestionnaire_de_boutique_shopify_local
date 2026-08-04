from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path as _BootstrapPath
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[1]))

from pathlib import Path
from tools.runtime_tool import emit
def main():
 root=Path(__file__).resolve().parents[1];files=[p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and 'build' not in p.parts];return emit({'files':len(files),'python':sum(p.suffix=='.py' for p in files),'cpp':sum(p.suffix in {'.cpp','.h'} for p in files),'graphql':sum(p.suffix=='.graphql' for p in files)})
if __name__=='__main__':raise SystemExit(main())
