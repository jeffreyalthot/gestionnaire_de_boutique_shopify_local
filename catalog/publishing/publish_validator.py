from __future__ import annotations


def validate_publish(product: dict[str, object]) -> dict[str, object]:
    failures=[]
    if not str(product.get("title", "")).strip(): failures.append("missing_title")
    if len(str(product.get("descriptionHtml", product.get("description", "")))) < 100: failures.append("description_short")
    if not product.get("variants"): failures.append("missing_variants")
    if not product.get("files") and not product.get("media"): failures.append("missing_media")
    if float(product.get("margin_percent", 0) or 0) < 40: failures.append("margin_below_minimum")
    if float(product.get("quality_score", 0) or 0) < .7: failures.append("quality_below_minimum")
    if product.get("compliance_status") not in {None, "passed"}: failures.append("compliance_not_passed")
    return {"passed": not failures, "failures": failures}
