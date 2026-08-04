def supplier_score(supplier: dict[str,object]) -> float:
    score=0.4
    if supplier.get("verified"): score+=0.3
    score+=min(float(supplier.get("years",0) or 0)/20,0.2)
    if float(supplier.get("response_rate",1) or 1)>=0.8: score+=0.1
    return min(1.0,round(score,4))
