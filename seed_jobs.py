import sqlite3

conn= sqlite3.connect('jobs.db')
cursor = conn.cursor()
# Insert sample job listings into the jobs table
jobs = [(
        "Data Analyst",
        "python:5,sql:4,statistics:3",
        "excel:2,tableau:1"
    ),
    (
        "Backend Developer",
        "python:5,django:4,sql:3",
        "docker:2,aws:1"
    ),
    (
        "Frontend Developer",
        "javascript:5,react:4,html:3,css:3",
        "typescript:2"
    ),
    (
        "Machine Learning Engineer",
        "python:5,ml:5,statistics:4",
        "deep learning:3,tensorflow:2"
    ),
    (
        "Data Scientist",
        "python:5,statistics:4,ml:4",
        "deep learning:3,sql:2"
    ),
    (
        "DevOps Engineer",
        "linux:5,docker:5,ci/cd:4",
        "aws:3,python:2"
    ),
    (
        "Mobile App Developer",
        "java:5,kotlin:4",
        "android studio:2"
    ),
    (
        "Cyber Security Analyst",
        "networking:5,security:5,linux:4",
        "python:2"
    ),
    (
        "Cloud Engineer",
        "aws:5,cloud:5,linux:4",
        "terraform:2"
    ),
    (
        "AI Researcher",
        "python:5,ml:5,math:4",
        "deep learning:3,pytorch:2"
    )
]

cursor.executemany("INSERT INTO jobs (title, required_skills, optional_skills) VALUES (?, ?, ?)", jobs)
conn.commit()
conn.close()

print("Jobs inserted successfully.")