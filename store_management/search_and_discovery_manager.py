class SearchAndDiscoveryManager:
    def synonyms(self,groups: list[list[str]]) -> tuple[tuple[str,...],...]:
        result=[];seen=set()
        for group in groups:
            normalized=tuple(sorted({str(x).strip().lower() for x in group if str(x).strip()}))
            if len(normalized)>=2 and normalized not in seen:result.append(normalized);seen.add(normalized)
        return tuple(result)
    def audit(self,groups: list[list[str]],max_group_size: int=20) -> dict[str,object]:
        normalized=self.synonyms(groups);issues=[]
        if any(len(group)>max_group_size for group in normalized):issues.append("synonym_group_too_large")
        terms=[term for group in normalized for term in group]
        if len(terms)!=len(set(terms)):issues.append("term_in_multiple_groups")
        return {"valid":not issues,"groups":normalized,"issues":tuple(issues)}
