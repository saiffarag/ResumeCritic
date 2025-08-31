import re

def passive_voice_ratio(text: str) -> float:
    tokens = re.findall(r"\b\w+\b", text)
    if not tokens:
        return 0.0
    matches = re.findall(r"\b(am|is|are|was|were|been|being|be)\s+\w+ed\b", text, flags=re.I)
    return min(1.0, len(matches) / max(1, len(tokens) / 20))

def quantify_hits(text: str) -> int:
    return len(re.findall(r"(\d+%|\$\d+[\d,]*|\b\d+ (users|requests|ms|s|hours|months)\b)", text))

def readability_grade(text: str) -> float:
    try:
        import textstat
        return float(textstat.flesch_kincaid_grade(text))
    except Exception:
        return 12.0

def jd_requirements(jd_text: str) -> list:
    import re
    bullets = [r.strip("- ").strip()
               for r in re.findall(r"^[\-\u2022•].+$", jd_text, flags=re.M)]
    if not bullets:
        bullets = [s.strip() for s in jd_text.split(".")]
    return [b for b in bullets if len(b.split()) > 2][:12]
