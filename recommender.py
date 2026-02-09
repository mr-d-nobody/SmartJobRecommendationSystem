import os
import sqlite3
from ml_matcher import build_job_text, compute_ml_scores


# -------------------------------------------------
# Absolute DB path (CRITICAL for Streamlit Cloud)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "jobs.db")


# -------------------------------------------------
# DB bootstrap (schema + seed)
# -------------------------------------------------
def ensure_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        required_skills TEXT NOT NULL,
        optional_skills TEXT
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM jobs")
    count = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    # Seed only once
    if count == 0:
        import seed_jobs


# -------------------------------------------------
# Utility functions
# -------------------------------------------------
def parse_skills(skill_string):
    skills = {}
    if not skill_string:
        return skills

    for skill in skill_string.split(","):
        name, weight = skill.split(":")
        skills[name.strip()] = int(weight)

    return skills


def calculate_job_score(user_skills, required_skills, optional_skills):
    matched_required = sum(
        weight for skill, weight in required_skills.items()
        if skill in user_skills
    )
    total_required = sum(required_skills.values())
    required_score = matched_required / total_required if total_required else 0

    matched_optional = sum(
        weight for skill, weight in optional_skills.items()
        if skill in user_skills
    )
    total_optional = sum(optional_skills.values())
    optional_score = matched_optional / total_optional if total_optional else 0

    final_score = (0.7 * required_score) + (0.3 * optional_score)
    return round(final_score * 100, 2)


# -------------------------------------------------
# Main recommender
# -------------------------------------------------
def recommend_jobs(user_skills, resume_text=None):
    ensure_db()  # 🔑 GUARANTEES DB + TABLE + DATA

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT title, required_skills, optional_skills FROM jobs"
    )
    jobs = cursor.fetchall()
    conn.close()

    recommendations = []
    job_texts = []
    parsed_jobs = []

    for title, req_str, opt_str in jobs:
        required = parse_skills(req_str)
        optional = parse_skills(opt_str)

        rule_score = calculate_job_score(
            user_skills, required, optional
        )

        job_text = build_job_text(title, required, optional)

        parsed_jobs.append({
            "title": title,
            "required": required,
            "optional": optional,
            "rule_score": rule_score,
            "job_text": job_text
        })

        job_texts.append(job_text)

    ml_scores = (
        compute_ml_scores(resume_text, job_texts)
        if resume_text else [0] * len(job_texts)
    )

    for job, ml_score in zip(parsed_jobs, ml_scores):
        final_score = round(
            (0.6 * job["rule_score"]) + (0.4 * ml_score),
            2
        )

        recommendations.append({
            "job": job["title"],
            "score": final_score,
            "rule_score": job["rule_score"],
            "ml_score": ml_score,
            "missing_required": [
                s for s in job["required"] if s not in user_skills
            ]
        })

    recommendations.sort(key=lambda x: x["score"], reverse=True)
    return recommendations


# -------------------------------------------------
# Skill helper
# -------------------------------------------------
def get_all_skills():
    ensure_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT required_skills, optional_skills FROM jobs"
    )
    rows = cursor.fetchall()
    conn.close()

    skills = set()
    for req, opt in rows:
        for block in (req, opt):
            if block:
                for item in block.split(","):
                    skills.add(item.split(":")[0].strip())

    return skills
