import streamlit as st
from skills_taxonomy import SKILL_TAXONOMY
from skill_extractor import extract_skills_from_taxonomy
from resume_parser import extract_text_from_pdf
from recommender import recommend_jobs 


st.title("Job Recommendation System")
st.write("Enter your skills (comma separated) and select additional skills:")

skill_text = st.text_input("Your Skills (e.g., python, sql, statistics):")

common_skills=[
    "python", "sql", "excel", "ml", "statistics",
    "django", "react", "docker", "aws", "linux", "java", "kotlin",
    "networking", "security", "cloud", "deep learning", "tableau", "ci/cd", "android studio", "pytorch"
]

checked_skills = st.multiselect(
    "Select skills you know",
    common_skills
)

st.subheader("📄 Upload Resume (PDF)")
resume_file = st.file_uploader("Upload your resume", type=["pdf"])

if st.button("Get Job Recommendations"):
    user_skills = []
    resume_text = None

    if resume_file:
        resume_text = extract_text_from_pdf(resume_file)
        user_skills = extract_skills_from_taxonomy(
            resume_text,
            SKILL_TAXONOMY
        )

        st.write("Extracted skills from resume:")
        st.write(user_skills)

    else:
        text_skills = [s.strip().lower() for s in skill_text.split(",") if s.strip()]
        user_skills = list(set(text_skills + checked_skills))

    if not user_skills:
        st.warning("No skills detected. Please upload a resume or enter skills.")
    else:
        results = recommend_jobs(
            user_skills=user_skills,
            resume_text=resume_text
        )

        st.subheader("🔍 Recommended Jobs")

        for job in results[:5]:
            st.markdown(f"### {job['job']}")
            st.write(f"Final Score: **{job['score']}%**")
            st.write(f"Rule Score: {job['rule_score']}%")
            st.write(f"ML Score: {job['ml_score']}%")

            if job["missing_required"]:
                st.write("Missing required skills:")
                st.write(", ".join(job["missing_required"]))
            else:
                st.write("You meet all required skills 🎉")

            st.divider()
