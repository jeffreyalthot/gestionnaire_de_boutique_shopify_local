def option_definitions(variants: list[dict[str,object]]) -> list[dict[str,object]]:
    names=[]
    for variant in variants:
        opts=variant.get("options",{})
        if isinstance(opts,dict):
            for name in opts:
                if name not in names: names.append(name)
    return [{"name":name,"values":[{"name":str(v["options"].get(name,""))} for v in variants if isinstance(v.get("options"),dict) and name in v["options"]]} for name in names]
