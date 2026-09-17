import os
from openai import OpenAI
from claims import extract_claims
from search import search_claim_both_sides
from sources import source_score
from verifier import verify_claim

def detect_news(text: str):
    model = os.getenv("OPENAI_MODEL", "gpt-5.6")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    claims = extract_claims(client, model, text)
    results = []

    for claim in claims[:12]:
        sources = search_claim_both_sides(claim["text"])
        for source in sources:
            source["source_score"] = source_score(source)

        verification = verify_claim(client, model, claim, sources)
        results.append({
            "claim": claim,
            "verdict": verification["verdict"],
            "confidence": verification["confidence"],
            "explanation": verification["explanation"],
            "evidence": verification["evidence"],
            "sources": sources,
        })

    return build_report(results)

def build_report(results):
    if not results:
        return {"verdict": "no_verificable", "confidence": 0,
                "summary": "No se encontraron afirmaciones factuales verificables.",
                "claims": []}

    weights = {"verdadero": 1, "falso": -1, "enganoso": -0.5, "no_verificable": 0}
    total = sum(max(.1, float(r["claim"].get("importance", .5))) for r in results)
    score = sum(
        weights.get(r["verdict"], 0) * max(.1, float(r["claim"].get("importance", .5)))
        for r in results
    ) / total

    if score <= -.45: verdict = "falso"
    elif score < -.1: verdict = "enganoso"
    elif score >= .45: verdict = "verdadero"
    else: verdict = "no_verificable"

    confidence = round(sum(
        float(r["confidence"]) * max(.1, float(r["claim"].get("importance", .5)))
        for r in results
    ) / total)

    return {
        "verdict": verdict,
        "confidence": confidence,
        "summary": f"Se analizaron {len(results)} afirmaciones por separado. Revisa cada afirmación y sus fuentes antes de sacar conclusiones.",
        "claims": results,
    }
