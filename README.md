# SmartJobRecommendationSystem

A web-based job recommendation system built using Python, SQLite, and Streamlit.

## Features
- Recommends job roles based on user skills
- Uses weighted required and optional skills
- Ranks jobs by match score
- Shows missing required skills for transparency
- Simple and interactive UI

## Tech Stack
- Python
- SQLite
- Streamlit

## How it works
1. User enters skills (text + checkboxes)
2. System compares skills with job requirements stored in a database
3. Jobs are ranked using a weighted scoring algorithm
4. Top job recommendations are displayed with explanations

## Run Locally
```bash
pip install streamlit
python db_setup.py
python seed_jobs.py
python -m streamlit run app.py
