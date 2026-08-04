from __future__ import annotations


class SEOAuditor:
    def audit(self, product: dict[str, object]) -> dict[str, object]:
        title = str(product.get("title", ""))
        description = str(product.get("description", product.get("descriptionHtml", "")))
        handle = str(product.get("handle", ""))
        issues = []
        if not 30 <= len(title) <= 70: issues.append("title_length")
        if len(description) < 150: issues.append("description_short")
        if not handle or len(handle) > 80: issues.append("handle")
        if not product.get("alt_texts"): issues.append("missing_alt_text")
        score = max(0, 100 - len(issues) * 20)
        return {"score": score, "issues": issues, "passed": score >= 80}
