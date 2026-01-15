from ml_matcher import build_job_text, compute_ml_scores


def parse_skills(skill_string):
    skills={}
    if not skill_string:
        return skills
    
    for skill in skill_string.split(','):
        name,weight=skill.split(':')
        skills[name.strip()]=int(weight)

    return skills

def calculate_job_score(user_skills,required_skills,optional_skills):
    #required skill scoring
    matched_required = 0
    total_required = sum(required_skills.values())

    for skill,weight in required_skills.items():
        if skill in user_skills:
            matched_required += weight

    required_score = (matched_required / total_required) if total_required else 0

    #optional skill scoring
    matched_optional = 0
    total_optional = sum(optional_skills.values())
    for skill,weight in optional_skills.items():
        if skill in user_skills:
            matched_optional += weight

    optional_score = (matched_optional / total_optional) if total_optional else 0

    #final score calculation
    final_score = (0.7 * required_score) + (0.3 * optional_score)
    return round(final_score*100,2)  #return score as percentage

import sqlite3

def recommend_jobs(user_skills, resume_text=None):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, required_skills, optional_skills FROM jobs")
    jobs = cursor.fetchall()
    conn.close()

    recommendations = []
    job_texts = []

    parsed_jobs = []

    for title, req_str, opt_str in jobs:
        required = parse_skills(req_str)
        optional = parse_skills(opt_str)

        rule_score = calculate_job_score(user_skills, required, optional)

        job_text = build_job_text(title, required, optional)

        parsed_jobs.append({
            "title": title,
            "required": required,
            "optional": optional,
            "rule_score": rule_score,
            "job_text": job_text
        })

        job_texts.append(job_text)

   
    if resume_text:
        ml_scores = compute_ml_scores(resume_text, job_texts)
    else:
        ml_scores = [0] * len(job_texts)

    # --- FINAL COMBINATION ---
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


def get_all_skills():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("SELECT required_skills, optional_skills FROM jobs")
    rows = cursor.fetchall()
    conn.close()

    skills = set()

    for req, opt in rows:
        for block in (req, opt):
            if block:
                for item in block.split(","):
                    skill = item.split(":")[0].strip()
                    skills.add(skill)

    return skills
