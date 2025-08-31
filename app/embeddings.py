from typing import List
import numpy as np

class Embedder:
    _model = None

    def __init__(self):
        if not Embedder._model:
            from sentence_transformers import SentenceTransformer
            Embedder._model = SentenceTransformer('all-MiniLM-L6-v2')

    def encode(self, texts: List[str]):
        return Embedder._model.encode(texts, normalize_embeddings=True)

def semantic_coverage(resume_bullets: List[str], jd_reqs: List[str]) -> float:
    if not resume_bullets or not jd_reqs:
        return 0.0
    emb = Embedder()
    B = emb.encode(resume_bullets)
    R = emb.encode(jd_reqs)
    scores = [float(np.max(np.dot(B, r))) for r in R]
    return 100.0 * (sum(scores) / len(scores))
