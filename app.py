import streamlit as st
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


if st.button("Get Job Recommendations"):
    # Process input skills
    text_skills = [s.strip().lower() for s in skill_text.split(",") if s.strip()]
    user_skills = list(set(text_skills + checked_skills))

    if not user_skills:
        st.warning("Please enter or select at least one skill.")
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