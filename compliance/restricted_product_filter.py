import re
_RULES={
"arme ou composant d'arme":r"\b(gun|firearm|ammunition|silencer|taser|switchblade)\b",
"substance contrôlée":r"\b(cannabis|cocaine|methamphetamine|fentanyl|psychedelic)\b",
"produit nicotiné":r"\b(vape|nicotine|cigarette|tobacco)\b",
"médicament réglementé":r"\b(prescription drug|steroid|ozempic|viagra)\b",
"contrefaçon probable":r"\b(replica|counterfeit|fake designer|1:1 copy)\b",
}
def restricted_reason(text: str) -> str:
    lowered=text.lower()
    for reason,pattern in _RULES.items():
        if re.search(pattern,lowered,re.I): return reason
    return ""
