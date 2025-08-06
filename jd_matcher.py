from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from model.gemma_runner import run_inference

def match_resume_to_jd(resume_text, jd_text):
    # vectorizer = TfidfVectorizer()
    # tfidf = vectorizer.fit_transform([resume_text, jd_text])
    # similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])
    # return float(similarity[0][0])
    return run_inference(resume_text, jd_text, task="match")