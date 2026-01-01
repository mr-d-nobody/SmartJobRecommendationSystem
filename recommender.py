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

def recommend_jobs(user_skills):
    conn=sqlite3.connect('jobs.db')
    cursor=conn.cursor()
    cursor.execute("SELECT title, required_skills, optional_skills FROM jobs")
    jobs=cursor.fetchall()

    conn.close()

    recommendations=[]

    for title,req_str,opt_str in jobs:
        required=parse_skills(req_str)
        optional=parse_skills(opt_str)
        score=calculate_job_score(user_skills,required,optional)
        recommendations.append({
            "job": title,
            "score": score,
            "missing_required": [
                s for s in required if s not in user_skills
            ]
        })


    recommendations.sort(key=lambda x:x["score"],reverse=True)
    return recommendations

