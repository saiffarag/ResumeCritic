from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
from app.schemas import AnalyzeResponse
from app.parsers import read_pdf, read_docx, extract_sections, extract_bullets
from app.heuristics import passive_voice_ratio, quantify_hits, readability_grade, jd_requirements
from app.embeddings import semantic_coverage
from app.scoring import compute_subscores, overall
from app import llm

app = FastAPI(title="AI Resume Critic")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    role_title: Optional[str] = Form(None),
    target_tone: Optional[str] = Form("confident, concise")
):
    raw = await resume.read()
    name = resume.filename.lower()
    if name.endswith(".pdf"):
        text = read_pdf(raw)
    elif name.endswith(".docx"):
        text = read_docx(raw)
    else:
        text = raw.decode(errors="ignore")

    sections = extract_sections(text)
    bullets = extract_bullets(text)
    jd_reqs = jd_requirements(job_description)

    pv = passive_voice_ratio(text)
    quant = quantify_hits(text)
    fk = readability_grade(text)
    coverage = semantic_coverage(bullets[:50], jd_reqs[:12])

    subs = compute_subscores(coverage, fk, pv, quant)
    base_overall = overall(subs)

    prompt = llm.build_prompt(role_title or "", jd_reqs, bullets, quant, fk, pv, target_tone or "")
    model_json = llm.generate_structured(prompt)

    # Merge deterministic subscores/overall with model suggestions
    response = AnalyzeResponse(
        overall_score=base_overall,
        subscores=subs,
        missing_keywords=model_json.get("missing_keywords", []),
        high_impact_fixes=model_json.get("high_impact_fixes", []),
        bullet_rewrites=model_json.get("bullet_rewrites", []),
        ats_flags=model_json.get("ats_flags", []),
        tone_suggestions=model_json.get("tone_suggestions", []),
        clarity_suggestions=model_json.get("clarity_suggestions", []),
    )
    return response
