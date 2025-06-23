from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from scoring import calculate_archetypes
from geminiai_helper import generate_document_from_quiz
from fastapi.middleware.cors import CORSMiddleware
from ats import extract_text_from_pdf, compute_similarity
from adzuna import get_job_roles_and_salaries
import tempfile
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======== Data Models ========
class QuizSubmission(BaseModel):
    answers: dict

class DocumentRequest(BaseModel):
    user_info: dict
    quiz_answers: dict

class JobSearchRequest(BaseModel):
    keywords: list[str]
    archetype: str | None = None
    location: str | None = "United States"

# ======== Routes ========

@app.post("/submit-quiz")
def submit_quiz(submission: QuizSubmission):
    try:
        result = calculate_archetypes(submission.answers)
        return {"results": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-cover-letter")
def generate_cover_letter(request: DocumentRequest):
    try:
        letter = generate_document_from_quiz(request.user_info, request.quiz_answers, mode="cover_letter")
        return {"cover_letter": letter}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-resume")
def generate_resume(request: DocumentRequest):
    try:
        resume = generate_document_from_quiz(request.user_info, request.quiz_answers, mode="resume")
        return {"resume": resume}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-resume")
async def analyze_resume(resume: UploadFile = File(...), jd: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as resume_tmp, tempfile.NamedTemporaryFile(delete=False) as jd_tmp:
            resume_tmp.write(await resume.read())
            jd_tmp.write(await jd.read())

        resume_text = extract_text_from_pdf(resume_tmp.name)
        jd_text = extract_text_from_pdf(jd_tmp.name)

        match_score = compute_similarity(resume_text, jd_text)
        common_keywords = list(set(jd_text.lower().split()) & set(resume_text.lower().split()))
        top_keywords = list(dict.fromkeys(common_keywords))[:3]

        roles_with_salary = get_job_roles_and_salaries(top_keywords)

        os.unlink(resume_tmp.name)
        os.unlink(jd_tmp.name)

        return {
            "match_score": f"{match_score}%",
            "top_roles": roles_with_salary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search-jobs")
def search_jobs(request: JobSearchRequest):
    try:
        results = get_job_roles_and_salaries(
            keywords=request.keywords,
            archetype=request.archetype,
            location=request.location
        )
        return {"jobs": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
