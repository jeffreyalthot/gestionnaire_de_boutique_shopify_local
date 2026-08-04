from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path as _BootstrapPath
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[1]))

from tools.runtime_tool import database,emit
from catalog.discovery.search_plan import SearchPlan
def main():
 s,_=database();queries=tuple(x.strip() for x in s.product_discovery_keywords.split(',') if x.strip());p=SearchPlan(queries,s.product_discovery_page_size,s.product_discovery_max_pages,s.product_discovery_max_candidates);return emit({'dry_run':True,'queries':p.queries,'max_candidates':p.max_candidates})
if __name__=='__main__':raise SystemExit(main())
