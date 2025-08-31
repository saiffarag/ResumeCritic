import json
from typing import Dict, Any, List

def build_prompt(role_title: str, jd_reqs: List[str], bullets: List[str],
                 quant: int, fk: float, pv: float, target_tone: str) -> str:
    return (
        f"ROLE_TITLE: {role_title or ''}\n"
        f"TOP JD REQUIREMENTS: {jd_reqs[:12]}\n"
        f"TOP BULLETS: {bullets[:10]}\n"
        f"METRICS_FOUND: {quant}\n"
        f"READABILITY_FK: {fk:.1f}\n"
        f"PASSIVE_RATIO: {pv:.2f}\n"
        f"TARGET_TONE: {target_tone}\n"
        "Return STRICT JSON with keys: overall_score (0-100), "
        "subscores {relevance, clarity, tone, ats, evidence}, missing_keywords[], "
        "high_impact_fixes[], bullet_rewrites[{original, improved, reason}], "
        "ats_flags[{flag, severity}], tone_suggestions[], clarity_suggestions[]."
    )

def generate_structured(prompt: str) -> Dict[str, Any]:
    # TODO: integrate OpenAI/Anthropic with JSON mode & retries
    # Safe fallback so the API always returns something valid
    return {
        "overall_score": 80,
        "subscores": {"relevance": 78, "clarity": 82, "tone": 75, "ats": 85, "evidence": 70},
        "missing_keywords": [],
        "high_impact_fixes": ["Quantify top 3 bullets."],
        "bullet_rewrites": [],
        "ats_flags": [],
        "tone_suggestions": [],
        "clarity_suggestions": []
    }
