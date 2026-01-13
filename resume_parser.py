import PyPDF2
import re

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "

    return text.lower()


def extract_skills_from_text(text, skill_set):
    found_skills = set()

    for skill in skill_set:
        # exact word match (avoids partial matches)
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found_skills.add(skill)

    return list(found_skills)
