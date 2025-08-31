def compute_subscores(coverage: float, fk: float, pv: float, quant: int) -> dict:
    relevance = round(0.6 * coverage + 40) if coverage > 0 else 50
    clarity = max(0, min(100, 100 - abs(fk - 10) * 7 - pv * 30))
    tone = max(0, min(100, 90 - pv * 40))
    ats = 80  # placeholder; replace with real ATS rule checks
    evidence = min(100, 60 + quant * 5)
    return {
        "relevance": int(relevance),
        "clarity": int(clarity),
        "tone": int(tone),
        "ats": int(ats),
        "evidence": int(evidence),
    }

def overall(subscores: dict) -> int:
    w = {"relevance":0.40, "clarity":0.25, "tone":0.15, "ats":0.15, "evidence":0.05}
    score = sum(w[k]*subscores[k] for k in w)
    return int(round(score))
