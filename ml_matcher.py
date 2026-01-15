from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_job_text(title, required_skills, optional_skills):
    """
    Converts job data into plain text for ML
    """
    req = " ".join(required_skills.keys())
    opt = " ".join(optional_skills.keys())

    text = f"""
    Job title is {title}.
    Required skills are {req}.
    Optional skills include {opt}.
    """
    return text.lower()


def compute_ml_scores(resume_text, job_texts):
    """
    resume_text: string
    job_texts: list of strings

    returns: list of similarity scores (0–100)
    """
    documents = [resume_text] + job_texts

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_df=0.9,
        min_df=1
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    resume_vector = tfidf_matrix[0]
    job_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(resume_vector, job_vectors)[0]

    return [round(score * 100, 2) for score in similarities]
