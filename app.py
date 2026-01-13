import streamlit as st
 
from resume_parser import extract_text_from_pdf, extract_skills_from_text
from recommender import recommend_jobs, get_all_skills

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

    # CASE 1: Resume uploaded
    if resume_file:
        text = extract_text_from_pdf(resume_file)
        all_skills = get_all_skills()
        user_skills = extract_skills_from_text(text, all_skills)

        st.write("Extracted skills from resume:")
        st.write(user_skills)

    # CASE 2: Manual input fallback
    else:
        text_skills = [s.strip().lower() for s in skill_text.split(",") if s.strip()]
        user_skills = list(set(text_skills + checked_skills))

    if not user_skills:
        st.warning("No skills detected. Please upload a resume or enter skills.")
    else:
        results = recommend_jobs(user_skills)

        st.subheader("🔍 Recommended Jobs")

        for job in results[:5]:
            st.markdown(f"### {job['job']}")
            st.write(f"Match Score: **{job['score']}%**")

            if job["missing_required"]:
                st.write("Missing required skills:")
                st.write(", ".join(job["missing_required"]))
            else:
                st.write("You meet all required skills 🎉")

            st.divider()
