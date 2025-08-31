import io
import re

def read_pdf(file_bytes: bytes) -> str:
    from pdfminer.high_level import extract_text
    with io.BytesIO(file_bytes) as f:
        return extract_text(f) or ""

def read_docx(file_bytes: bytes) -> str:
    import docx
    with io.BytesIO(file_bytes) as f:
        doc = docx.Document(f)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_sections(text: str) -> dict:
    headers = ["summary", "experience", "work experience", "projects", "education", "skills"]
    chunks = {"header": ""}
    last = 0
    last_name = "header"
    for m in re.finditer(r"^(.*)$", text, flags=re.M):
        line = m.group(1).strip()
        if line and line.lower() in headers:
            chunks[last_name] = text[last: m.start()].strip()
            last = m.end()
            last_name = line.lower()
    chunks[last_name] = text[last:].strip()
    return chunks

def extract_bullets(text: str) -> list:
    return [b.strip("- •\u2022").strip()
            for b in re.findall(r"^[\-•\u2022].+$", text, flags=re.M)]
