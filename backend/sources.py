from urllib.parse import urlparse

PRIMARY_DOMAINS = {
    "boe.es", "europa.eu", "who.int", "un.org", "ine.es",
    "ec.europa.eu", "data.europa.eu"
}

def source_score(source: dict) -> float:
    domain = urlparse(source["url"]).netloc.lower()
    score = 50.0
    if any(domain == d or domain.endswith("." + d) for d in PRIMARY_DOMAINS):
        score += 30
    if not source.get("snippet"):
        score -= 15
    return max(0.0, min(100.0, score))
