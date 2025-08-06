# Technical Writeup (Proof of Work)

## Overview
This project presents a Private AI Hiring Assistant that utilizes **Gemma 3n** to perform resume-job description matching and interview question generation while 
preserving user privacy via on-device inference served through a secure tunnel (**ngrok**). The system is designed to help recruiters assess resume relevance and 
prepare interview questions based on the candidate's qualifications — all without sending sensitive data to cloud APIs.

## System Architecture
**1. Frontend (Streamlit App)**
- Accepts user input:
     -> PDF Resume Upload
     -> Job Description (JD) Text

- Displays:
     -> Resume-JD Match Score
     -> Technical/Soft Skill Extraction
     -> Interview Questions based on the resume & JD
  
**2. Resume Text Extraction**
- Implemented in resume_parser.py
- Uses PyMuPDF to extract text from PDF resumes
- Ensures accurate extraction even from structured resumes

**3. Backend Inference Handler**
- File: gemma_runner.py
- Sends JSON payload to a local instance of Gemma 3n hosted via ngrok
- Payload includes:
     -> Resume text
     -> JD text
     -> Task type (either "match" or "chat")
     -> Optional query for chat tasks

**4. Gemma 3n LLM**
- Hosted locally to preserve privacy and reduce API costs
- Tasks:
     -> match: Returns a structured JSON including technical skills, experience, education, soft skills, and an overall match score
     -> chat: Generates follow-up interview questions
- Prompt structure:
  
  `
  [RESUME]
...resume text...
[JD]
...job description...
[OUTPUT]
  `
  
## Data Flow Diagram
```
[User Interface - Streamlit]
         │
         ▼
[Extract Resume Text from PDF]
         │
         ▼
[Send resume + JD to gemma_runner.py]
         │
         ▼
[Call ngrok → Gemma 3n backend]
         │
         ▼
[Gemma 3n processes & returns JSON response]
         │
         ▼
[Streamlit displays:
 - Match Score
 - Technical Skills
 - Interview Questions
]
```

## Example Output

```
{
  "Technical Skills": [
  "Data Science", "Python", "React", ...
  ],
  "Relevant Experience": ["2023", "2024"],
  "Education": ["BTech", "2024"],
  "Soft Skills": ["Teamwork", "Problem Solving"],
  "Match Score": "85 / 100"
}
```

## Why Gemma 3n?
Gemma 3n was chosen for the following reasons:
-> **Lightweight & Open-source**: Perfect for local deployment, especially where privacy is essential.
-> **Highly Capable for Instruction Tasks**: Despite its smaller size, Gemma 3n performs well for structured tasks like skill extraction and Q&A.
-> **Free of API Rate Limits**: By self-hosting, the app can run without latency or cost issues.

## Technical Choices & Justification

| Component              | Technology       | Justification                                           |
| ---------------------- | ---------------- | ------------------------------------------------------- |
| **Frontend**           | Streamlit        | Rapid prototyping with interactivity; easy file uploads |
| **PDF Parsing**        | PyMuPDF (`fitz`) | Fast and accurate resume text extraction                |
| **Model Serving**      | ngrok + requests | Secure and simple connection to locally running LLM     |
| **Gemma 3n**           | Fine-tuned LLM   | Lightweight enough for local use; avoids exposing PII   |
| **Structured Prompts** | Custom Templates | Consistent formatting to guide LLM outputs              |

## Challenges Overcome
 1. Unstructured Resume Text
- Resumes vary in format. Extracting meaningful text required careful selection of PDF libraries.
- Solved using PyMuPDF for reliable block-level text extraction.

2. Handling JSON Parsing from LLM
- Sometimes the LLM output was semi-structured or malformed.
- Introduced prompt instruction for strict JSON outputs like:

`
Your output should only contain JSON. No explanation.
`

3. Privacy & Security
- To avoid exposing resumes and JD to cloud APIs:
     -> Hosted the model locally using ngrok
     -> Avoided using any OpenAI or external API calls

4. Model Prompt Tuning
- Had to experiment with prompt phrasing to get structured outputs reliably.
- Balanced clarity with brevity to stay within model context limits.

## Results
- Successfully outputs Match Score and skills with structured JSON
- Generates custom interview questions dynamically based on resume-JD alignment
- Preserves data privacy by keeping everything local
- Can scale to handle multiple tasks (e.g., JD classification, resume enhancement) with small prompt changes

## Future Enhancements
- Add fine-tuning or RAG for domain-specific hiring (e.g., healthcare, finance)
- Provide visual analytics (skill overlap, word clouds)
- Store previous sessions locally for recruiters to review

## Appendix: Key Prompts Used

**1. Match Score Prompt**
```
[RESUME]
...resume text...
[JD]
...job description...
[OUTPUT]

Your output should be JSON formatted like:
{
  "Technical Skills": [...],
  "Relevant Experience": [...],
  "Education": [...],
  "Soft Skills": [...],
  "Match Score": "X / 100"
}
```

**2. Interview Question Prompt**
```
[RESUME]
...resume text...
[JD]
...job description...
[INTERVIEW_QUESTIONS]

Generate 5 technical and 3 behavioral questions that test the candidate's suitability.
```
