import streamlit as st
from resume_parser import extract_text_from_pdf
# from app.jd_matcher import match_resume_to_jd
# from app.interview_prep import generate_questions
from model.gemma_runner import run_inference

st.title("Private AI Hiring Assistant")

resume_file = st.file_uploader("Upload resume (PDF)", type=["pdf"])
jd_text = st.text_area("Paste Job Description")

if st.button("Analyze"):
    if resume_file is None or jd_text.strip()=="":
        st.warning("Please upload a resume and provide a job description")
    else:
        resume_text = extract_text_from_pdf(resume_file)

        if not resume_text:
            st.error("Could not extract text from the uploaded pdf")
        else:
            # Match score from Gemma
            st.subheader("Match Score")
            match_prompt = f"""[RESUME]\n{resume_text}\n[JD]\n{jd_text}\n[OUTPUT]"""
            score_output = run_inference(resume_text, jd_text)
            st.success(f"Model Response: {score_output}")

            # Interview questions from Gemma
            st.subheader("Interview Questions")
            qa_prompt = f"""[RESUME]\n{resume_text}\n[JD]\n{jd_text}\n[INTERVIEW_QUESTIONS]"""
            questions = run_inference(resume_text, jd_text).replace("INTERVIEW_QUESTIONS", "").strip()
            st.write(questions)