import sqlite3

conn= sqlite3.connect('jobs.db')
cursor = conn.cursor()
# Insert sample job listings into the jobs table
jobs = [

    # ===== DATA / AI =====
    ("Data Analyst", "python:5,sql:4,statistics:3", "excel:2,tableau:1"),
    ("Senior Data Analyst", "python:5,sql:5,statistics:4", "power bi:2,tableau:2"),
    ("Data Scientist", "python:5,statistics:4,ml:4", "deep learning:3,sql:2"),
    ("Machine Learning Engineer", "python:5,ml:5,statistics:4", "deep learning:3,tensorflow:2"),
    ("AI Researcher", "python:5,ml:5,math:4", "deep learning:3,pytorch:2"),
    ("NLP Engineer", "python:5,nlp:5,ml:4", "deep learning:3"),
    ("Computer Vision Engineer", "python:5,ml:4", "deep learning:3,opencv:2"),
    ("Business Intelligence Analyst", "sql:5,statistics:4", "tableau:3,power bi:2"),
    ("Data Engineer", "python:5,sql:4", "aws:3,spark:2"),
    ("Analytics Engineer", "sql:5,python:4", "dbt:2"),

    # ===== BACKEND =====
    ("Backend Developer", "python:5,django:4,sql:3", "docker:2,aws:1"),
    ("Senior Backend Developer", "python:5,django:5,sql:4", "docker:3,aws:2"),
    ("API Developer", "python:5,backend:4", "flask:3"),
    ("Java Backend Engineer", "java:5,sql:4", "spring:3"),
    ("Microservices Engineer", "backend:5,docker:4", "kubernetes:3"),

    # ===== FRONTEND =====
    ("Frontend Developer", "javascript:5,react:4,html:3,css:3", "typescript:2"),
    ("Senior Frontend Developer", "javascript:5,react:5,html:4,css:4", "typescript:3"),
    ("UI Developer", "html:5,css:5,javascript:4", "react:2"),
    ("Web Developer", "html:5,css:4,javascript:4", "backend:2"),
    ("Full Stack Developer", "javascript:5,python:4,sql:3", "react:3,django:3"),

    # ===== DEVOPS / CLOUD =====
    ("DevOps Engineer", "linux:5,docker:5,ci/cd:4", "aws:3,python:2"),
    ("Senior DevOps Engineer", "linux:5,docker:5,ci/cd:5", "kubernetes:4"),
    ("Cloud Engineer", "aws:5,cloud:5,linux:4", "terraform:2"),
    ("Cloud Architect", "cloud:5,aws:5", "docker:3"),
    ("Site Reliability Engineer", "linux:5,cloud:4", "ci/cd:3"),

    # ===== MOBILE =====
    ("Mobile App Developer", "java:5,kotlin:4", "android studio:2"),
    ("Android Developer", "kotlin:5,java:4", "android studio:3"),
    ("Mobile Software Engineer", "java:4,kotlin:4", "backend:2"),

    # ===== SECURITY / NETWORK =====
    ("Cyber Security Analyst", "networking:5,security:5,linux:4", "python:2"),
    ("Security Engineer", "security:5,networking:4", "cloud:3"),
    ("SOC Analyst", "security:5,networking:4", "linux:3"),
    ("Network Engineer", "networking:5,linux:4", "cloud:2"),

    # ===== DATABASE =====
    ("Database Administrator", "sql:5,linux:4", "cloud:2"),
    ("SQL Developer", "sql:5,python:3", "data analysis:2"),

    # ===== QA / SUPPORT =====
    ("QA Engineer", "testing:5", "automation:3"),
    ("Automation Tester", "testing:5,python:3", "selenium:3"),
    ("Technical Support Engineer", "linux:4,networking:4", "cloud:2"),

    # ===== GENERAL TECH =====
    ("Software Engineer", "programming:5", "python:3"),
    ("Junior Software Engineer", "programming:4", "python:2"),
    ("IT Engineer", "linux:4,networking:4", "cloud:2"),
]


cursor.executemany("INSERT INTO jobs (title, required_skills, optional_skills) VALUES (?, ?, ?)", jobs)
conn.commit()
conn.close()

print("Jobs inserted successfully.")