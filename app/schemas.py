from pydantic import BaseModel
from typing import List, Dict

class AnalyzeResponse(BaseModel):
    overall_score: int
    subscores: Dict[str, int]
    missing_keywords: List[str]
    high_impact_fixes: List[str]
    bullet_rewrites: List[Dict[str, str]]
    ats_flags: List[Dict[str, str]]
    tone_suggestions: List[str]
    clarity_suggestions: List[str]
