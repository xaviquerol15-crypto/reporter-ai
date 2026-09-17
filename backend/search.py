import os
import requests
from urllib.parse import urlparse

def search_claim(claim: str, max_results: int = 8):
    api_key = os.getenv("SEARCH_API_KEY")
    if not api_key:
        return []

    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": api_key,
            "query": claim,
            "search_depth": "advanced",
            "max_results": max_results,
            "include_answer": False,
        },
        timeout=30,
    )
    response.raise_for_status()

    results = []
    for item in response.json().get("results", []):
        url = item.get("url", "")
        if url:
            results.append({
                "title": item.get("title", ""),
                "url": url,
                "domain": urlparse(url).netloc.lower(),
                "snippet": item.get("content", "")[:5000],
            })
    return results

def search_claim_both_sides(claim: str):
    queries = [claim, f"evidence contradicting or fact check: {claim}"]
    merged, seen = [], set()
    for query in queries:
        for result in search_claim(query):
            if result["url"] not in seen:
                seen.add(result["url"])
                merged.append(result)
    return merged[:12]
