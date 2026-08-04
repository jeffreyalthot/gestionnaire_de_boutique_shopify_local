class OrderTagService:
    def merge(self, existing: list[str] | tuple[str,...], additions: list[str] | tuple[str,...], removals: list[str] | tuple[str,...]=()) -> tuple[str,...]:
        removed={x.strip().lower() for x in removals}
        tags={x.strip() for x in (*existing,*additions) if x.strip() and x.strip().lower() not in removed}
        return tuple(sorted(tags,key=str.lower))
