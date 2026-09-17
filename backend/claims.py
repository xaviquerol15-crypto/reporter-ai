import json
from openai import OpenAI

def extract_claims(client: OpenAI, model: str, text: str):
    prompt = f"""
Eres el módulo de extracción de afirmaciones de Reporter AI.

Texto:
{text}

Extrae afirmaciones factuales que puedan comprobarse externamente.
Separa afirmaciones complejas. No extraigas opiniones, preguntas,
predicciones ni valoraciones subjetivas.

Devuelve SOLO JSON:
{{
  "claims": [
    {{"id": 1, "text": "afirmación comprobable", "importance": 0.0}}
  ]
}}

importance está entre 0 y 1.
"""
    response = client.responses.create(model=model, input=prompt)
    return json.loads(response.output_text).get("claims", [])
