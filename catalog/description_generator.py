import html
def generate_description(title: str,attributes: dict[str,object],source_description: str="") -> str:
    bullets="".join(f"<li><strong>{html.escape(str(k))}:</strong> {html.escape(str(v))}</li>" for k,v in attributes.items() if v)
    body=html.escape(source_description.strip()) if source_description else f"Découvrez {html.escape(title)}, sélectionné selon nos critères de qualité et de disponibilité."
    return f"<p>{body}</p><ul>{bullets}</ul><p>Le délai et le tarif de livraison sont calculés selon la destination.</p>"
