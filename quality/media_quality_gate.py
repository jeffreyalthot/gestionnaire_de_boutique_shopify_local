class MediaQualityGate:
    def evaluate(self,media: list[dict[str,object]],minimum_images: int=1,minimum_dimension: int=800) -> dict[str,object]:
        issues=[];hashes=set();valid=0
        if len(media)<minimum_images:issues.append("missing_media")
        for i,item in enumerate(media):
            width=int(item.get("width",0) or 0);height=int(item.get("height",0) or 0);kind=str(item.get("content_type",item.get("type","image")))
            if kind.startswith("image") and (width<minimum_dimension or height<minimum_dimension):issues.append(f"low_resolution_{i}")
            digest=str(item.get("sha256",item.get("hash","")))
            if digest and digest in hashes:issues.append(f"duplicate_{i}")
            hashes.add(digest);valid+=not any(x.endswith(f"_{i}") for x in issues)
        score=valid/max(1,len(media));return {"allowed":not issues and len(media)>=minimum_images,"score":round(score,4),"issues":tuple(issues),"count":len(media)}
