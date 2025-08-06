from model.gemma_runner import run_inference

def generate_questions(resume_text, jd_text):
    # gemma = GemmaModel()
    # prompt = f"""
    # You are an interviewer. Based on the following resume and job description generate 5 interview questions:

    # Resume: {resume_text}
    # Job Description: {jd_text}
    # """
    # return gemma.generate(prompt)
    # Custom prompt
    # prompt = f"[RESUME]\n{resume_text}\n[JD]\n{jd_text}\n[INTERVIEW_QUESTIONS]"
    return run_inference(resume_text, jd_text, task="qa")