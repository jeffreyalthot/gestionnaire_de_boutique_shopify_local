class LocationManager:
    def active(self,locations: list[dict[str,object]]) -> tuple[dict[str,object],...]:return tuple(dict(x) for x in locations if x.get("active",True))
    def audit(self,locations: list[dict[str,object]]) -> dict[str,object]:
        issues=[];seen=set()
        for index,item in enumerate(locations):
            ident=str(item.get("id","") or item.get("name","")).strip()
            if not ident:issues.append(f"location_{index}_missing_identity")
            if ident in seen:issues.append(f"location_{index}_duplicate")
            seen.add(ident)
            if item.get("active",True) and not item.get("address"):issues.append(f"location_{index}_missing_address")
        return {"valid":not issues,"active":len(self.active(locations)),"issues":tuple(issues)}
