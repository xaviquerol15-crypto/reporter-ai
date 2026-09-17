import json

VALID = {"verdadero", "falso", "enganoso", "no_verificable"}

def verify_claim(client, model, claim, sources):
    evidence_text = "\n\n".join(
        f"""SOURCE
Title: {s['title']}
URL: {s['url']}
Domain: {s['domain']}
Source score (heuristic): {s['source_score']}
Text: {s['snippet']}
"""
        for s in sources
    )

    prompt = f"""
Reporter AI verifica esta afirmación:

"{claim['text']}"

EVIDENCIA RECUPERADA:
{evidence_text or "No se recuperó evidencia web."}

Reglas:
- No inventes fuentes, URLs, citas ni hechos.
- Repetir la afirmación no constituye confirmación independiente.
- Considera fecha, jurisdicción, magnitud, causalidad y contexto.
- Si la evidencia es insuficiente, usa no_verificable.
- Usa engañoso cuando el contexto o alcance cambie materialmente el significado.
- Usa únicamente URLs presentes en la evidencia recuperada.

Devuelve SOLO JSON:
{{
  "verdict": "verdadero|falso|enganoso|no_verificable",
  "confidence": 0,
  "explanation": "explicación breve",
  "evidence": [
    {{"url": "URL exacta", "supports": true, "strength": 0,
     "explanation": "por qué apoya o contradice"}}
  ]
}}
"""
    response = client.responses.create(model=model, input=prompt)
    result = json.loads(response.output_text)
    if result.get("verdict") not in VALID:
        result["verdict"] = "no_verificable"

    allowed = {s["url"] for s in sources}
    result["evidence"] = [
        e for e in result.get("evidence", []) if e.get("url") in allowed
    ]
    return result
